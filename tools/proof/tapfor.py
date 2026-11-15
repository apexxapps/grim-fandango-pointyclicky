#!/usr/bin/env python3
"""tapfor.py <feet x> <feet y> <ds>: a tap above Manny's line (tr, setup 2) that targets ds units along the push (+) / pull (-),
from Manny's feet as the moment logs them; also prints the barrow's t (0 = push end; hoses: box1 .75-.85, box2 1.15-1.26,
box3 1.52-1.63, box4 1.82-1.95)."""
import sys
sys.path.insert(0, '/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/tools/proof')
import proj
M0 = (3.59296, 1.71733); D = (-0.3968275, 0.9178932)   # Manny at the push end; the pull direction (his facing, 203.4 deg, reversed)
def scr(t):
    return proj.P('tr', 2, [(M0[0] + D[0] * t, M0[1] + D[1] * t, -1.77)])[0]
fx, fy, ds = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
ts = [k / 100 for k in range(-50, 300)]
pts = proj.P('tr', 2, [(M0[0] + D[0] * t, M0[1] + D[1] * t, -1.77) for t in ts])
t_now = min(ts, key=lambda t: (pts[ts.index(t)][0] - fx) ** 2 + (pts[ts.index(t)][1] - fy) ** 2)
t_to = t_now - ds
x, y = scr(t_to)
x2, y2 = scr(t_to + 0.05)
dx, dy = x2 - x, y2 - y
L = (dx * dx + dy * dy) ** .5
nx, ny = dy / L, -dx / L
if ny > 0:
    nx, ny = -nx, -ny
print('%d %d   barrow t now %.2f -> %.2f' % (round(x + nx * 110), round(y + ny * 110), t_now, t_to))
