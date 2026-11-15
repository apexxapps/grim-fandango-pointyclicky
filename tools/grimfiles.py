"""Reading Grim Fandango's own files: LAB archives and BM / ZBM images.

Used by the tools that check the edition against the game (inventory.py,
sheets.py). They read the player's own copy; nothing is copied into the repo.
The formats follow ScummVM's engines/grim (lab.cpp, bitmap.cpp).
"""
import os
import re
import struct
import zlib


class Lab:
    """One of the game's .LAB archives: names, offsets, sizes. From a file, or
    from bytes already in memory (the update's DATA005.LAB)."""

    def __init__(self, path, data=None):
        self.path, self.data = path, data
        if data is not None:
            head, rest = data[:16], data[16:]
        else:
            with open(path, 'rb') as f:
                head, rest = f.read(16), None
        if head[:4] != b'LABN':
            raise ValueError(f'{path}: not a LAB')
        _, n, nl = struct.unpack('<III', head[4:16])
        if rest is not None:
            dirb, names = rest[:16 * n], rest[16 * n:16 * n + nl]
        else:
            with open(path, 'rb') as f:
                f.seek(16)
                dirb = f.read(16 * n)
                names = f.read(nl)
        self.files = {}
        for i in range(n):
            no, off, size, _ = struct.unpack('<IIII', dirb[16 * i:16 * i + 16])
            name = names[no:names.index(b'\0', no)].decode('latin-1')
            self.files[name.lower()] = (off, size)

    def read(self, name):
        off, size = self.files[name.lower()]
        if self.data is not None:
            return self.data[off:off + size]
        with open(self.path, 'rb') as f:
            f.seek(off)
            return f.read(size)


def update_files(path):
    """The files inside LucasArts' 1.01 update (gfupd101.exe), by name, as
    ScummVM reads it (engines/grim/update: packfile.cpp, mscab.cpp): a
    cabinet behind a "1CNT" container whose bytes are scrambled by a table
    from a seed, MSZIP blocks. The game's own DATA005.LAB is in it ("@@_",
    for every language), and the engine reads it ahead of DATA000-004: ten
    of the game's scripts (_system, al, at, bd ... th) are its versions."""
    d = open(path, 'rb').read()
    for at in (0x1c000, 0x21000, 0x23000, 0x24000):
        if d[at:at + 4] == b'1CNT':
            break
    else:
        raise ValueError(f'{path}: no 1CNT container')
    v = struct.unpack('<I', d[at + 4:at + 8])[0]
    table = []
    for _ in range(256):
        v = (0x343FD * v + 0x269EC3) & 0xffffffff
        table.append((v >> 16) & 0x7fff)
    body = bytearray(d[at + 8:])
    for r, t in enumerate(table):   # each byte: XOR the low half, minus the high
        tr = bytes(((b ^ (t & 0xff)) - (t >> 8)) & 0xff for b in range(256))
        body[r::256] = body[r::256].translate(tr)
    cab = bytes(body)
    if cab[:4] != b'MSCF':
        raise ValueError(f'{path}: no cabinet')
    files_at = struct.unpack('<I', cab[16:20])[0]
    nfolders, nfiles, flags = struct.unpack('<HHH', cab[26:32])
    p, res_folder, res_data = 36, 0, 0
    if flags & 4:
        res_head, res_folder, res_data = struct.unpack('<HBB', cab[36:40])
        p = 40 + res_head
    folders = []
    for _ in range(nfolders):
        start, nblocks, comp = struct.unpack('<IHH', cab[p:p + 8])
        if comp & 0xf != 1:
            raise ValueError(f'{path}: not MSZIP')
        out, q = bytearray(), start
        for _ in range(nblocks):
            clen, _ulen = struct.unpack('<HH', cab[q + 4:q + 8])
            q += 8 + res_data
            block = cab[q:q + clen]
            q += clen
            z = zlib.decompressobj(-15, zdict=bytes(out[-32768:]))
            out += z.decompress(block[2:]) + z.flush()   # 'CK', then deflate
        folders.append(bytes(out))
        p += 8 + res_folder
    files, p = {}, files_at
    for _ in range(nfiles):
        size, offset, folder = struct.unpack('<IIH', cab[p:p + 10])
        end = cab.index(b'\0', p + 16)
        name = cab[p + 16:end].decode('latin-1')
        files[name] = folders[folder][offset:offset + size]
        p = end + 1
    return files


class Game:
    """Every DATA LAB of a Grim install, in the engine's order: the 1.01
    update's DATA005.LAB (from gfupd101.exe) wins over DATA004 ... DATA000."""

    def __init__(self, folder):
        self.labs = [Lab(os.path.join(folder, f)) for f in sorted(os.listdir(folder))
                     if re.match(r'(?i)data\d+\.lab$', f)]
        upd = [f for f in os.listdir(folder) if f.lower() == 'gfupd101.exe']
        if upd:
            for name, data in update_files(os.path.join(folder, upd[0])).items():
                if re.match(r'(?i)(@@_|common/)?data\d+\.lab$', name):
                    self.labs.append(Lab(f'{upd[0]}:{name}', data))

    def find(self, name):
        for lab in reversed(self.labs):
            if name.lower() in lab.files:
                return lab
        return None

    def read(self, name):
        lab = self.find(name)
        return lab.read(name) if lab else None

    def names(self, ext):
        return sorted({n for lab in self.labs for n in lab.files if n.endswith(ext)})


def _codec3(src, size):
    """bitmap.cpp's decompress_codec3: an LZ with a 16-bit flag stream."""
    out = bytearray()
    pos = 0
    bits = src[0] | src[1] << 8
    nbits = 16
    pos = 2

    def bit():
        nonlocal bits, nbits, pos
        b = bits & 1
        bits >>= 1
        nbits -= 1
        if nbits == 0:
            bits = src[pos] | src[pos + 1] << 8
            nbits = 16
            pos += 2
        return b

    while len(out) < size:
        if bit():
            out.append(src[pos])
            pos += 1
            continue
        if bit() == 0:
            length = 2 * bit()
            length += bit() + 3
            offset = src[pos] - 0x100
            pos += 1
        else:
            offset = (src[pos] | (src[pos + 1] & 0xf0) << 4) - 0x1000
            length = (src[pos + 1] & 0xf) + 3
            pos += 2
            if length == 3:
                length = src[pos] + 1
                pos += 1
                if length == 1:
                    break
        for _ in range(length):
            out.append(out[len(out) + offset])
    return bytes(out[:size])


def bitmap(data):
    """A BM or ZBM: (width, height, [16-bit values]) of its first image."""
    if data[:8] != b'BM  F\0\0\0':
        raise ValueError('not a Grim BM')
    codec, _, nimages = struct.unpack('<III', data[8:20])
    bpp = struct.unpack('<I', data[36:40])[0]
    width, height = struct.unpack('<II', data[128:136])
    pos = 128 + 8
    size = bpp // 8 * width * height
    if codec == 0:
        raw = data[pos:pos + size]
    elif codec == 3:
        n = struct.unpack('<I', data[pos:pos + 4])[0]
        raw = _codec3(data[pos + 4:pos + 4 + n], size)
    else:
        raise ValueError(f'unknown codec {codec}')
    return width, height, struct.unpack(f'<{width * height}H', raw)


def rgb565_ppm(width, height, px):
    """A BM's pixels as a binary PPM (RGB565 -> RGB888)."""
    out = bytearray(b'P6 %d %d 255\n' % (width, height))
    for v in px:
        out += bytes(((v >> 11) * 255 // 31, ((v >> 5) & 63) * 255 // 63, (v & 31) * 255 // 31))
    return bytes(out)


def zdepth(v):
    """A ZBM value as distance along the camera's view, in world units.
    Fitted against the game's own objects (14 Nov 2026: 87 objects in 6 sets
    agree with 65536/v - 1). 7 marks "no depth drawn here" (far)."""
    if v <= 7 or v == 0xf81f:
        return float('inf')
    return 65536.0 / v - 1.0
