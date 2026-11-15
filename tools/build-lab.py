#!/usr/bin/env python3
"""Builds grim-pointyclicky.lab, the PointyClicky Edition's data for Grim Fandango.

    python3 -I tools/build-lab.py --game <grim folder> [out.lab]   # default: build/grim-pointyclicky.lab

<grim folder> is the player's own copy (DATA000-004.LAB and gfupd101.exe, the
1.01 update the engine reads DATA005.LAB from); GRIM_GAME in the environment
does as well. Every .patchr is checked against the file the engine will
read for it (the update's version where it has one): a patch that fits no
such file would be skipped by the engine, so the build stops instead.

Packs, in one LAB archive (the format of Grim's own DATA00x.LAB):
  data/lab/*       the 71 script/costume patches (.patchr, applied by the
                   engine to LucasArts' own files, ScummVM's grim-patch.lab
                   fixes merged in), the 91 cursor / inventory images (.tga)
                   and mouse.lua (Lua 3.1 bytecode; its source is data/scripts/mouse.lua,
                   and recompiling it gives the same bytes)
  set.bin          generated here from data/hotspots/*.set.hot, the hand-drawn hotspot
                   polygons (one line per hotspot:
                   setup id "name" type numpos (x y z)*numpos npts (x y)*npts,
                   640x480 game pixels per camera setup)

Built on Grim Mouse, Tobias Pfaff's (2014-2016, GPL-2.0-or-later,
https://github.com/tobiaspfaff/grim_mouse); see README.md and CREDITS.md.
"""
import hashlib
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grimfiles  # noqa: E402
ROOT = os.path.join(HERE, '..')
OUT = os.path.join(ROOT, 'build', 'grim-pointyclicky.lab')


def string(s):
    b = s.encode('latin-1')
    return struct.pack('<i', len(b)) + b


def set_bin(hs_dir):
    """The same layout as Grim Mouse's script/convert_to_bin.py."""
    sets = []
    for name in sorted(os.listdir(hs_dir)):
        if not name.endswith('.set.hot'):
            continue
        rows = []
        with open(os.path.join(hs_dir, name), encoding='latin-1') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                start, _, rest = line.partition('"')
                desc, _, end = rest.partition('"')
                setup, _, hid = start.strip().partition(' ')
                tok = end.split()
                htype, npos = int(tok[0]), int(tok[1])
                pos = [float(t) for t in tok[2:2 + npos * 3]]
                npts = int(tok[2 + npos * 3])
                poly = [int(t) for t in tok[3 + npos * 3:3 + npos * 3 + npts * 2]]
                rows.append((hid, desc, int(setup), htype, pos, poly))
        sets.append((name[:-len('.hot')], rows))
    out = struct.pack('<i', len(sets))
    for set_name, rows in sets:
        out += string(set_name) + struct.pack('<i', len(rows))
        for hid, desc, setup, htype, pos, poly in rows:
            out += string(hid) + string(desc)
            out += struct.pack('<iii', setup, htype, len(pos) // 3)
            out += b''.join(struct.pack('<f', p) for p in pos)
            out += struct.pack('<i', len(poly) // 2)
            out += b''.join(struct.pack('<i', p) for p in poly)
    return out


def write_lab(path, entries):
    names = b''
    offsets = []
    for name, _ in entries:
        offsets.append(len(names))
        names += name.encode('latin-1') + b'\0'
    pos = 16 + 16 * len(entries) + len(names)
    directory = b''
    for (name, data), off in zip(entries, offsets):
        directory += struct.pack('<IIII', off, pos, len(data), 0)
        pos += len(data)
    with open(path, 'wb') as f:
        f.write(b'LABN' + struct.pack('<III', 0x10000, len(entries), len(names)))
        f.write(directory + names)
        for _, data in entries:
            f.write(data)


def check_patches(data_dir, game_dir):
    """Each patch chain (x.patchr, x_1.patchr ...) must have one patch whose
    target (size, md5 of the first 5000 bytes: engines/grim/patchr.cpp) is
    the file the engine reads. Returns the problems, one line each."""
    game = grimfiles.Game(game_dir)
    chains = {}
    for name in os.listdir(data_dir):
        m = re.match(r'(.+?)(_\d+)?\.patchr$', name)
        if m:
            chains.setdefault(m.group(1), []).append(name)
    bad = []
    for target, patches in sorted(chains.items()):
        orig = game.read(target)
        if orig is None:
            bad.append(f'{target}: not in the game')
            continue
        fits = []
        for pn in patches:
            head = open(os.path.join(data_dir, pn), 'rb').read(48)
            size = struct.unpack('<I', head[28:32])[0]
            fits.append(size == len(orig) and hashlib.md5(orig[:5000]).digest() == head[12:28])
        if not any(fits):
            bad.append(f'{target}: no patch fits the game\'s copy ({len(orig)} bytes, '
                       f'from {os.path.basename(game.find(target).path)})')
    return bad, len(chains)


def main():
    args = sys.argv[1:]
    game_dir = os.environ.get('GRIM_GAME')
    if '--game' in args:
        i = args.index('--game')
        game_dir = args[i + 1]
        del args[i:i + 2]
    if not game_dir:
        sys.exit('build-lab: give the game folder (--game <folder> or GRIM_GAME): '
                 'every script patch is checked against it')
    out = args[0] if args else OUT
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    data_dir = os.path.join(ROOT, 'data', 'lab')
    bad, n = check_patches(data_dir, game_dir)
    if bad:
        sys.exit('build-lab: the engine would skip these patches:\n  ' + '\n  '.join(bad))
    print(f'patches: all {n} fit the game\'s copy')
    entries = []
    for name in sorted(os.listdir(data_dir)):
        with open(os.path.join(data_dir, name), 'rb') as f:
            entries.append((name, f.read()))
    entries.append(('set.bin', set_bin(os.path.join(ROOT, 'data', 'hotspots'))))
    entries.sort(key=lambda e: e[0])
    write_lab(out, entries)
    print('%s: %d files, %d bytes' % (os.path.relpath(out), len(entries), os.path.getsize(out)))


if __name__ == '__main__':
    sys.exit(main())
