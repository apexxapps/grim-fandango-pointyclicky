#!/usr/bin/env python3
"""The edition's cursors, drawn pixel by pixel: white shapes with a one-pixel
black edge, flat, for Grim's 640x480 screen. Roles after the Remaster's set
(looked at 14 Nov 2026), our own drawing:

  cursor0  at rest          a thin crosshair, open in the middle
  cursor1  over a thing     a starburst
  cursor2  exit / walk      a block arrow, up (into the scene)
  cursor3..6                block arrows right, left, up, down (puzzles, conversations)
  cursor7  busy             a ring of dots

    python3 -I tools/cursors.py        # -> data/lab/cursor0..7.tga (+ _hl copies)

The _hl files (Grim Mouse's "flash every hotspot" look) are written the same:
the edition has no flash (discovery is Manny's head).
"""
import math
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
N = 32


def blank():
    return [[0] * N for _ in range(N)]


def rect(g, x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= x < N and 0 <= y < N:
                g[y][x] = 1


def line(g, x0, y0, x1, y1, w=2):
    steps = max(1, int(max(abs(x1 - x0), abs(y1 - y0)) * 2))
    for i in range(steps + 1):
        t = i / steps
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        rect(g, round(x - (w - 1) / 2), round(y - (w - 1) / 2), round(x - (w - 1) / 2) + w - 1, round(y - (w - 1) / 2) + w - 1)


def crosshair():
    g = blank()
    rect(g, 15, 3, 16, 11)
    rect(g, 15, 20, 16, 28)
    rect(g, 3, 15, 11, 16)
    rect(g, 20, 15, 28, 16)
    return g


def starburst():
    g = blank()
    for k in range(8):
        a = k * math.pi / 4
        r0, r1 = (6, 13) if k % 2 == 0 else (6, 11)
        line(g, 15.5 + r0 * math.cos(a), 15.5 + r0 * math.sin(a), 15.5 + r1 * math.cos(a), 15.5 + r1 * math.sin(a))
    return g


def arrow_up():
    g = blank()
    for y in range(4, 15):                 # head: a triangle, 1:1 slope
        half = y - 4
        rect(g, 15 - half, y, 16 + half, y)
    rect(g, 11, 15, 20, 27)                # shaft
    return g


def rotate(g, quarter):
    for _ in range(quarter % 4):
        g = [[g[N - 1 - x][y] for x in range(N)] for y in range(N)]
    return g


def ring():
    g = blank()
    for k in range(8):
        a = k * math.pi / 4 - math.pi / 2
        x, y = round(15.5 + 10 * math.cos(a)), round(15.5 + 10 * math.sin(a))
        rect(g, x - 1, y - 1, x + 1, y + 1)
    return g


def outlined(g):
    """RGBA rows: white shape, black one-pixel edge (8-neighbourhood), clear elsewhere."""
    rows = []
    for y in range(N):
        row = []
        for x in range(N):
            if g[y][x]:
                row.append((255, 255, 255, 255))
            elif any(0 <= x + dx < N and 0 <= y + dy < N and g[y + dy][x + dx]
                     for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                row.append((0, 0, 0, 255))
            else:
                row.append((0, 0, 0, 0))
        rows.append(row)
    return rows


def write(rows, path):
    """Uncompressed 32-bit TGA, as Grim Mouse's own: bottom-up rows, BGRA, 8 alpha bits."""
    head = bytes([0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, N, 0, N, 0, 32, 0x08])
    body = bytes(c for row in reversed(rows) for (r, g, b, a) in row for c in (b, g, r, a))
    with open(path, 'wb') as f:
        f.write(head + body)


def main():
    up = arrow_up()
    shapes = [crosshair(), starburst(), up, rotate(up, 1), rotate(up, 3), up, rotate(up, 2), ring()]
    out = os.path.join(ROOT, 'data', 'lab')
    for i, g in enumerate(shapes):
        rows = outlined(g)
        write(rows, os.path.join(out, f'cursor{i}.tga'))
        write(rows, os.path.join(out, f'cursor{i}_hl.tga'))
    print('cursor0..7.tga ->', os.path.relpath(out))


if __name__ == '__main__':
    main()
