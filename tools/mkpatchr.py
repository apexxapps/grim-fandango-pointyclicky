#!/usr/bin/env python3
"""Writes a .patchr (the format ScummVM's Grim engine patches the game's files
with, engines/grim/patchr.cpp) that turns <original> into <new>: the inverse of
patchr.py.

    python3 -I tools/mkpatchr.py <original> <new> <out.patchr>

Only the differences travel: the bytes the two files share are XORed to zero,
what <new> inserts is carried as it is, and what it drops is jumped over. So
a patch carries the edition's changes, never the game's own file.
The result is checked by applying it with patchr.py.
"""
import difflib
import gzip
import hashlib
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchr  # noqa: E402


def make(orig, new):
    ops = difflib.SequenceMatcher(None, orig, new, autojunk=False).get_opcodes()
    # The layout Grim Mouse's patches use (flag 1: the diff and the extra bytes
    # in one stream, triple by triple; the control triples uncompressed): the
    # engine's PatchedFile only rewinds that one stream when it seeks back.
    ctrl, data = [], bytearray()
    cur = [0, bytearray(), bytearray(), 0]   # diff copy, its XOR bytes, extra bytes, jump

    def flush():
        if cur[0] or cur[2] or cur[3]:
            ctrl.append((cur[0], len(cur[2]), cur[3]))
            data.extend(cur[1])
            data.extend(cur[2])
        cur[:] = [0, bytearray(), bytearray(), 0]

    for tag, i1, i2, j1, j2 in ops:
        n_old, n_new = i2 - i1, j2 - j1
        # a run of same-length change is copied and XORed, like an equal run
        same = min(n_old, n_new) if tag == 'replace' else (n_old if tag == 'equal' else 0)
        if same:
            if cur[2] or cur[3]:
                flush()
            cur[0] += same
            cur[1] += bytes(a ^ b for a, b in zip(orig[i1:i1 + same], new[j1:j1 + same]))
        if n_new > same:
            if cur[3]:
                flush()
            cur[2] += new[j1 + same:j2]
        if n_old > same:
            cur[3] += n_old - same
    flush()
    c = b''.join(struct.pack('<IIi', *t) for t in ctrl)
    zd = gzip.compress(bytes(data), 9, mtime=0)   # gzip: the engine takes the size from its trailer
    head = b'PATR' + struct.pack('<HHI', 2, 0, 1) + hashlib.md5(orig[:5000]).digest()
    head += struct.pack('<IIIII', len(orig), len(new), len(c), len(zd), 0)
    return head + c + zd


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    orig, new = (open(p, 'rb').read() for p in sys.argv[1:3])
    out = make(orig, new)
    if patchr.apply(orig, out) != new:
        sys.exit('mkpatchr: the patch does not give the new file back')
    open(sys.argv[3], 'wb').write(out)
    print('%s: %d bytes' % (sys.argv[3], len(out)))


if __name__ == '__main__':
    main()
