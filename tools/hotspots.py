#!/usr/bin/env python3
"""Writes data/hotspots/*.set.hot from the game itself: every object's outline
on every angle you play in (tools/outlines.py), checked, simplified and put
first; Grim Mouse's hand-drawn polygons kept only where a trace fails a check
and the game's own point is inside them; its walk paths and special-mode
regions kept as they are, after the objects.

    python3 -I tools/hotspots.py            # after inventory.py and outlines.py

Checks on a traced outline (else Grim Mouse's, else left out and listed):
  - it covers the game's own point for the thing (within 6 px);
  - not a sliver: at least 5 px wide and tall;
  - not far bigger than the thing: its area under 6x the object's reach on
    screen (a disc of its `range`), so a trace that ran across a wall or a
    floor doesn't swallow the room.
Priority (the engine takes the first hotspot that contains the pointer):
objects and doors, then walk paths, then the rest.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inventory as inv  # noqa: E402
import outlines as ol  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
HS = os.path.join(ROOT, 'data', 'hotspots')


def rdp(pts, eps=1.5):
    """Ramer-Douglas-Peucker, on a closed outline."""
    if len(pts) < 4:
        return pts

    def simplify(seg):
        if len(seg) < 3:
            return seg
        (x1, y1), (x2, y2) = seg[0], seg[-1]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1
        far, idx = 0, 0
        for i in range(1, len(seg) - 1):
            d = abs(dy * seg[i][0] - dx * seg[i][1] + x2 * y1 - y2 * x1) / n
            if d > far:
                far, idx = d, i
        if far > eps:
            return simplify(seg[:idx + 1])[:-1] + simplify(seg[idx:])
        return [seg[0], seg[-1]]
    half = len(pts) // 2
    out = simplify(pts[:half + 1])[:-1] + simplify(pts[half:] + [pts[0]])[:-1]
    return out if len(out) >= 3 else pts


def area(poly):
    return abs(sum(poly[i][0] * poly[i - 1][1] - poly[i - 1][0] * poly[i][1] for i in range(len(poly)))) / 2


def check(poly, su, obj, at=None):
    if at is not None and inv.distance(at, poly) > 6:
        return "it doesn't cover the game's own point for the thing"
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    if max(xs) - min(xs) < 5 or max(ys) - min(ys) < 5:
        return 'a sliver'
    r = ol.reach_px(su, obj['pos'], obj['range'] or 0.3)
    if area(poly) > 6 * math.pi * r * r:
        return f'{int(area(poly))} px against a reach of {int(math.pi * r * r)}'
    return None


def line(setup, hid, name, htype, poly, pos=(0, 0, 0)):
    pts = ' '.join(f'{x} {y}' for x, y in poly)
    return f'{setup} /{hid} "{name}" {htype} 1 {pos[0]} {pos[1]} {pos[2]} {len(poly)} {pts}'


def main():
    outl = json.load(open(os.path.join(ROOT, 'build', 'outlines', 'outlines.json')))
    objs = inv.objects(os.path.join(ROOT, 'build', 'inventory', 'lua'))
    raw = os.path.join(ROOT, 'build', 'inventory', 'raw')
    by = {}
    for r in outl:
        by.setdefault(r['set'], []).append(r)
    stats = {'traced': 0, 'kept': 0, 'left out': 0}
    review = []
    sets = sorted(set(by) | {f[:-len('.set.hot')] for f in os.listdir(HS) if f.endswith('.set.hot')})
    for st in sets:
        path = os.path.join(HS, st + '.set.hot')
        gm = inv.hotspots(path)
        sus = inv.setups(os.path.join(raw, st + '.set')) if os.path.exists(os.path.join(raw, st + '.set')) else []
        out, covered = [], set()
        for r in sorted(by.get(st, []), key=lambda r: (r['setup'], r['object'])):
            o = objs[st][r['object']]
            if not o['id']:
                continue
            htype = 2 if 'walkOut' in o['handlers'] else 1
            name = o['name'] or r['name']
            poly, why = None, None
            if r['how'] in ('depth', 'surface', 'carried') and r['poly']:
                poly = rdp([tuple(p) for p in r['poly']])
                why = check(poly, sus[r['setup']], o, r['at'])
                if why:
                    poly = None
            if poly:
                stats['traced'] += 1
            else:
                mine = [h for h in gm if h['setup'] == r['setup'] and h['id'] == o['id'] and len(h['poly']) >= 3]
                if mine and any(inv.inside(r['at'], h['poly']) for h in mine):
                    poly = max(mine, key=lambda h: len(h['poly']))['poly']
                    stats['kept'] += 1
                else:
                    stats['left out'] += 1
                    review.append({'set': st, 'setup': r['setup'], 'object': r['object'], 'how': r['how'],
                                   'why': why or r.get('why'), 'at': r['at']})
                    continue
            out.append(line(r['setup'], o['id'], name, htype, poly))
            covered.add((r['setup'], o['id']))
        # Grim Mouse's own: objects we had no view for, then walk paths, then special modes.
        for h in gm:
            if h['type'] in (1, 2) and (h['setup'], h['id']) not in covered and h['id'] not in ('to',):
                out.append(raw_line(path, h))
        for h in gm:
            if h['type'] == 3 or h['id'] == 'to':
                out.append(raw_line(path, h))
        for h in gm:
            if h['type'] >= 4 and h['type'] != 3:
                out.append(raw_line(path, h))
        if out:
            open(path, 'w', encoding='latin-1').write('\n'.join(dict.fromkeys(out)) + '\n')
    json.dump(review, open(os.path.join(ROOT, 'build', 'outlines', 'review.json'), 'w'), indent=1)
    print(f"traced {stats['traced']}, Grim Mouse's kept {stats['kept']}, left out {stats['left out']} (build/outlines/review.json)")


_RAW = {}


def raw_line(path, h):
    """A hotspot's line exactly as it is in the file (walk paths keep their 3D path)."""
    if path not in _RAW:
        _RAW[path] = [l.rstrip('\n') for l in open(path, encoding='latin-1') if l.strip()]
    for l in _RAW[path]:
        start, _, rest = l.partition('"')
        setup, _, hid = start.strip().partition(' ')
        name, _, after = rest.partition('"')
        # the type too: an object and its walk path (or Grim Mouse's
        # actor-following copy) can share setup, id and name
        if (int(setup) == h['setup'] and hid.strip('/') == h['id'] and name == h['name'] and
                int(after.split()[0]) == h['type']):
            return l
    return line(h['setup'], h['id'], h['name'], h['type'], h['poly'])


if __name__ == '__main__':
    sys.exit(main())
