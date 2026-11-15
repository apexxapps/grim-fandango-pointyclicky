#!/usr/bin/env python3
"""The edition's cursor: Simon's bone crosshair (14 Nov 2026), pixel for pixel.

One bone, drawn as he drew the top one, mirrored and turned for the other
three, with the light from the top left; no centre dot (Simon). 26x26, drawn
centred on the pointer by the engine, in Manny's own bone colours.

Two states only, the way LucasArts did it in the late 90s, while Manny's
head does the discovering (docs/PLAN.md):
  cursor0          at rest: bone
  cursor1, 2       over a thing / an exit: marigold
  cursor3..6       puzzles and conversations: marigold (Grim Mouse's arrow slots)
  cursor7          cut-scenes: nothing (the original showed no pointer)

    python3 -I tools/cursors.py        # -> data/lab/cursor0..7.tga (+ _hl copies)
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
N = 26
TOP = [  # 10 wide, columns 8..17; row 0 is the bone's outer end. K ink, C bone, T shadow, G mid-tone
    '..KKKKKK..',
    '..KGCCTK..',
    'KKKGCCTKKK',
    'KGGCCCCTTK',
    'KGCCCCTTTK',
    'KKKCCCTTKK',
    '..KCCCTK..',
    '..KCCCTK..',
    '...KCTK...',
    '...KCTK...',
    '....KK....',
]
# Manny's own bone (14 Nov 2026): m_bone.mat / m_jaw.mat through suit.cmp, his costume's colour map.
REST = {'K': (17, 7, 0), 'C': (247, 245, 231), 'T': (198, 194, 177), 'G': (226, 227, 213)}
HOT = {'K': (17, 7, 0), 'C': (242, 160, 61), 'T': (164, 94, 18), 'G': (255, 206, 130)}   # Grim's theme accent, the Day of the Dead's marigold (Simon 15 Nov 2026)


def grid():
    g = {}
    for r, row in enumerate(TOP):
        for i, ch in enumerate(row):
            if ch != '.':
                x, y = 8 + i, r
                g[(x, y)] = ch                # top
                g[(x, N - 1 - y)] = ch        # bottom: mirrored up-down
                g[(y, x)] = ch                # left: the top on its side
                g[(N - 1 - y, x)] = ch        # right: the left mirrored
    return g


def write(g, pal, path):
    """Uncompressed 32-bit TGA, as Grim Mouse's own: bottom-up rows, BGRA, 8 alpha bits."""
    head = bytes([0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, N, 0, N, 0, 32, 0x08])
    body = bytearray()
    for y in reversed(range(N)):
        for x in range(N):
            if pal and (x, y) in g:
                r, gg, b = pal[g[(x, y)]]
                body += bytes((b, gg, r, 255))
            else:
                body += b'\0\0\0\0'
    with open(path, 'wb') as f:
        f.write(head + bytes(body))


def main():
    g = grid()
    out = os.path.join(ROOT, 'data', 'lab')
    for i in range(8):
        pal = REST if i == 0 else None if i == 7 else HOT
        for suffix in ('', '_hl'):
            write(g, pal, os.path.join(out, f'cursor{i}{suffix}.tga'))
    print('cursor0..7.tga ->', os.path.relpath(out))


if __name__ == '__main__':
    main()
