"""Reading Grim Fandango's own files: LAB archives and BM / ZBM images.

Used by the tools that check the edition against the game (inventory.py,
sheets.py). They read the player's own copy; nothing is copied into the repo.
The formats follow ScummVM's engines/grim (lab.cpp, bitmap.cpp).
"""
import os
import re
import struct


class Lab:
    """One of the game's .LAB archives: names, offsets, sizes."""

    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            head = f.read(16)
            if head[:4] != b'LABN':
                raise ValueError(f'{path}: not a LAB')
            _, n, nl = struct.unpack('<III', head[4:16])
            dirb = f.read(16 * n)
            names = f.read(nl)
        self.files = {}
        for i in range(n):
            no, off, size, _ = struct.unpack('<IIII', dirb[16 * i:16 * i + 16])
            name = names[no:names.index(b'\0', no)].decode('latin-1')
            self.files[name.lower()] = (off, size)

    def read(self, name):
        off, size = self.files[name.lower()]
        with open(self.path, 'rb') as f:
            f.seek(off)
            return f.read(size)


class Game:
    """Every DATA LAB of a Grim install; later LABs win, as in the engine."""

    def __init__(self, folder):
        self.labs = [Lab(os.path.join(folder, f)) for f in sorted(os.listdir(folder))
                     if re.match(r'(?i)data\d+\.lab$', f)]

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
