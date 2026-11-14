#!/usr/bin/env python3
"""The edition's cursor: Simon's bone crosshair (14 Nov 2026), pixel for pixel.

One bone, drawn as he drew the top one, mirrored and turned for the other
three, with the light from the top left; a small bone dot in the middle.
40x40, drawn centred on the pointer by the engine.

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
N = 40
TOP = [  # 12 wide, columns 14..25; row 0 is the bone's outer end. K ink, C bone, T shadow, G glint
    '..KKKKKKKK..',
    '..KGCCCCTK..',
    '..KGCCCCTK..',
    'KKKGCCCCTKKK',
    'KGGGCCCCTGGK',
    'KGCCCCCCCTTK',
    'KGCCCCCTTTTK',
    'KKKCCCCTTKKK',
    '..KCCCCTTK..',
    '..KCCCCTTK..',
    '...KCCCTK...',
    '...KCCCTK...',
    '...KCCCTK...',
    '....KCTK....',
    '....KCTK....',
    '....KCTK....',
    '.....KK.....',
]
REST = {'K': (18, 14, 14), 'C': (250, 230, 194), 'T': (206, 182, 138), 'G': (226, 170, 74)}
HOT = {'K': (18, 14, 14), 'C': (255, 178, 52), 'T': (214, 120, 24), 'G': (255, 226, 120)}


def grid():
    g = {}
    for r, row in enumerate(TOP):
        for i, ch in enumerate(row):
            if ch != '.':
                x, y = 14 + i, r
                g[(x, y)] = ch                # top
                g[(x, N - 1 - y)] = ch        # bottom: mirrored up-down
                g[(y, x)] = ch                # left: the top on its side
                g[(N - 1 - y, x)] = ch        # right: the left mirrored
    for y in range(18, 22):                    # the dot: 2x2 bone, inked round
        for x in range(18, 22):
            g[(x, y)] = 'C' if 19 <= x <= 20 and 19 <= y <= 20 else 'K'
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
