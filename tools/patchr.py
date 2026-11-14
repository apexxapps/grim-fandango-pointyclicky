#!/usr/bin/env python3
"""Applies a .patchr (the format ScummVM's Grim engine patches the game's files
with, engines/grim/patchr.cpp) to a file, so a patched script can be read.

    python3 -I tools/patchr.py <original> <file.patchr> <out>

PATR v2: a 48-byte header (signature, version, flags, the target's md5 of
its first 5000 bytes and size, the new size, three stream lengths), then
three zlib streams: control triples (diff copy, extra copy, jump), the diff
bytes (XORed onto the original's) and the extra bytes (inserted as they are;
the same stream as the diff when flag 1 is set).
"""
import hashlib
import struct
import sys
import zlib


def inflate(data):
    try:
        return zlib.decompress(data)
    except zlib.error:
        return zlib.decompress(data, 16 + zlib.MAX_WBITS)   # gzip-wrapped


def apply(orig, patch):
    if patch[:4] != b'PATR':
        raise ValueError('not a patchr')
    major, minor, flags = struct.unpack('<HHI', patch[4:12])
    md5 = patch[12:28]
    size, new_size, zctrl, zdata, zextra = struct.unpack('<IIIII', patch[28:48])
    if hashlib.md5(orig[:5000]).digest() != md5 or len(orig) != size:
        raise ValueError('this patch is for a different file')
    p = 48
    ctrl = patch[p:p + zctrl]
    ctrl = inflate(ctrl) if flags & 2 else ctrl
    p += zctrl
    diff = inflate(patch[p:p + zdata])
    p += zdata
    extra = diff if flags & 1 else inflate(patch[p:p + zextra])
    out = bytearray()
    fpos = dpos = 0
    epos = 0
    for i in range(0, len(ctrl), 12):
        dcopy, ecopy, jump = struct.unpack('<IIi', ctrl[i:i + 12])
        chunk = bytearray(orig[fpos:fpos + dcopy])
        src = diff if not flags & 1 else diff
        for k in range(dcopy):
            chunk[k] ^= src[dpos + k]
        out += chunk
        fpos += dcopy
        dpos += dcopy
        if flags & 1:
            out += diff[dpos:dpos + ecopy]
            dpos += ecopy
        else:
            out += extra[epos:epos + ecopy]
            epos += ecopy
        fpos += jump
    return bytes(out[:new_size])


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    o, pt, dst = sys.argv[1:]
    open(dst, 'wb').write(apply(open(o, 'rb').read(), open(pt, 'rb').read()))
