#!/usr/bin/env python3
"""Outlines from the game itself: every object's shape on every angle you play
in, traced from the angle's depth image around the point where the game's
scripts put the object.

    python3 -I tools/outlines.py <grim folder> [set ...]     # after inventory.py

Writes build/outlines/outlines.json and build/outlines/<set>-<setup>.png
sheets (git-ignored: derived from the game's art). Each outline says how it
was made:
  depth     grown from the object's point while the depth stays continuous
            and within the object's own band (its range) of its distance
  surface   for surfaces seen edge-on (a cabinet's side): every pixel within
            the object's projected reach whose depth is within its band,
            connected to the point
  carried   traced on another angle where its depth exists, lifted into 3D
            and projected here (angles whose depth image only covers part
            of the scene)
  kept      nothing to trace, and Grim Mouse's outline holds the game's point
  actor     a character (key ends _obj): outlined live from its 3D model
  flag      none of these gave a believable shape (too small, too big, nothing
            drawn in the depth image): needs a person, listed for review
"""
import collections
import json
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grimfiles  # noqa: E402
import inventory as inv  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W, H = 640, 480
MIN_AREA, MAX_AREA = 120, 0.30 * W * H
FONT = next((f for f in ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc')
             if os.path.exists(f)), None)


def camera_depth(su, p):
    return inv.dot(inv.norm(inv.sub(su['interest'], su['position'])), inv.sub(p, su['position']))


def reach_px(su, p, r):
    """The object's range, as pixels on screen at its distance."""
    d = max(0.05, camera_depth(su, p))
    tan_x = math.tan(su['fov'] / 2 * math.pi / 180)
    return max(12, r / d / tan_x * W / 2)


def seed(D, pt, d0):
    x0, y0 = int(pt[0]), int(pt[1])
    cands = [(abs(D[y * W + x] - d0), x, y) for y in range(max(0, y0 - 8), min(H, y0 + 9))
             for x in range(max(0, x0 - 8), min(W, x0 + 9)) if D[y * W + x] != float('inf')]
    return min(cands)[1:] if cands else None


def grow(D, start, d0, band, radius=None, continuous=True):
    x0, y0 = start
    seen = {start}
    q = collections.deque([start])
    while q:
        x, y = q.popleft()
        d = D[y * W + x]
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in seen:
                continue
            if radius and (nx - x0) ** 2 + (ny - y0) ** 2 > radius * radius:
                continue
            nd = D[ny * W + nx]
            if nd == float('inf') or abs(nd - d0) >= band:
                continue
            if continuous and abs(nd - d) >= 0.01 * d:
                continue
            seen.add((nx, ny))
            q.append((nx, ny))
    return seen


def close(region, r=3):
    """Morphological closing: fills the gaps between carried points."""
    grown = set()
    for x, y in region:
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                grown.add((x + dx, y + dy))
    keep = set()
    for x, y in grown:
        if all((x + dx, y + dy) in grown for dx, dy in ((r, 0), (-r, 0), (0, r), (0, -r))):
            keep.add((x, y))
    return {p for p in keep if 0 <= p[0] < W and 0 <= p[1] < H}


def largest(region):
    """The biggest connected piece of a region."""
    left, best = set(region), set()
    while left:
        start = left.pop()
        part, q = {start}, collections.deque([start])
        while q:
            x, y = q.popleft()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in left:
                    left.discard(n)
                    part.add(n)
                    q.append(n)
        if len(part) > len(best):
            best = part
    return best


def hull(region):
    """Convex hull (monotone chain) of a region's pixels."""
    pts = sorted(set(region))
    if len(pts) < 3:
        return pts

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and turn(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and turn(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def polygon(region, step=2):
    """A simple outline: each row's left edge down, right edge back up."""
    rows = collections.defaultdict(list)
    for x, y in region:
        rows[y].append(x)
    ys = sorted(rows)[::step]
    left = [(min(rows[y]), y) for y in ys]
    right = [(max(rows[y]), y) for y in reversed(ys)]
    return left + right


def trace(D, su, o, pt):
    d0 = camera_depth(su, o['pos'])
    band = max(0.12, o['range'] * 0.5)
    s = seed(D, pt, d0)
    if not s:
        return 'flag', 'no depth drawn here', None
    reg = grow(D, s, d0, band)
    if MIN_AREA <= len(reg) <= MAX_AREA:
        return 'depth', None, reg
    reg2 = grow(D, s, d0, band * 0.5, radius=0.6 * reach_px(su, o['pos'], o['range'] or 0.3), continuous=False)
    if MIN_AREA <= len(reg2) <= MAX_AREA:
        return 'surface', None, reg2
    why = f'traced {len(reg)} / {len(reg2)} px'
    return 'flag', why, None


def basis(su):
    pos, interest = su['position'], su['interest']
    up = [0, 1, 0] if (pos[0] == interest[0] and pos[1] == interest[1]) else [0, 0, 1]
    f = inv.norm(inv.sub(interest, pos))
    s = inv.norm(inv.cross(f, up))
    return f, s, inv.cross(s, f), math.tan(su['fov'] / 2 * math.pi / 180), math.radians(su.get('roll', 0.0))


def unproject(su, region, D, step=3):
    """Pixels with depth back into world points (HotspotMan::raycast, depth along the view)."""
    f, s, u, tan_x, roll = basis(su)
    cr, sr = math.cos(roll), math.sin(roll)
    pts = []
    for (x, y) in region:
        if x % step or y % step:
            continue
        d = D[y * W + x]
        nx = 2 * (x + 0.5) / W - 1
        ny = 2 * (H - y - 0.5) / H - 1
        rx, ry = nx * tan_x, ny * 0.75 * tan_x
        ex, ey = cr * rx - sr * ry, sr * rx + cr * ry
        pts.append([su['position'][k] + (s[k] * ex + u[k] * ey + f[k]) * d for k in range(3)])
    return pts


def reproject(su, cloud, D=None):
    """A world point cloud as a screen region on another angle (hidden points dropped where depth exists)."""
    reg = set()
    f = basis(su)[0]
    for p in cloud:
        pt = inv.project(su, p)
        if not pt:
            continue
        x, y = int(pt[0]), int(pt[1])
        if D:
            d = inv.dot(f, inv.sub(p, su['position']))
            if D[y * W + x] < d - max(0.05, 0.03 * d):
                continue
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if 0 <= x + dx < W and 0 <= y + dy < H:
                    reg.add((x + dx, y + dy))
    return reg


def run(game, st, raw, objs, report, out):
    path = os.path.join(raw, st + '.set')
    sus = inv.setups(path)
    cams = inv.camera_sectors(path)
    bgs, cur = {}, None
    for line in open(path, encoding='latin-1'):
        t = line.split()
        if t[:1] == ['setup']:
            cur = t[1]
        elif t[:1] == ['background'] and cur:
            bgs[cur] = t[1]
    hid = {(m['setup'], m['object']) for m in report.get(st, {}).get('hidden', [])}
    ours = inv.hotspots(os.path.join(ROOT, 'data', 'hotspots', st + '.set.hot'))
    results = []
    depths, clouds = {}, collections.defaultdict(list)
    for i, su in enumerate(sus):
        if not inv.in_play(su, cams) or not su.get('zbuffer'):
            continue
        try:
            _, _, z = grimfiles.bitmap(game.read(su['zbuffer']))
        except Exception:
            continue
        depths[i] = [grimfiles.zdepth(v) for v in z]
    # Pass 1: every object traced where its angle has depth; its shape kept as 3D points.
    for i, D in depths.items():
        su = sus[i]
        for key, o in objs.get(st, {}).items():
            if (o['pos'] == [0, 0, 0] and o['range'] == 0) or (i, key) in hid:
                continue
            pt = inv.project(su, o['pos'])
            if pt:
                how, _, reg = trace(D, su, o, pt)
                if reg:
                    clouds[key] += unproject(su, reg, D)
    for i, D in depths.items():
        su = sus[i]
        draw = []
        regions, kept_polys = {}, {}
        for key, o in sorted(objs.get(st, {}).items()):
            if (o['pos'] == [0, 0, 0] and o['range'] == 0) or (i, key) in hid:
                continue
            pt = inv.project(su, o['pos'])
            if not pt:
                continue
            how, why, reg = trace(D, su, o, pt)
            kept_poly = None
            if how == 'flag' and clouds.get(key):
                reg2 = reproject(su, clouds[key], D if why != 'no depth drawn here' else None)
                reg2 = close(reg2)
                if MIN_AREA <= len(reg2) <= MAX_AREA:
                    how, why, reg = 'carried', None, reg2
            if how == 'flag':
                gm = [h for h in ours if h['setup'] == i and h['id'] == o['id'] and len(h['poly']) >= 3]
                if gm and any(inv.inside(pt, h['poly']) for h in gm):
                    how, why = 'kept', None
                    reg = {(x, y) for x, y in max(gm, key=lambda h: len(h['poly']))['poly']}
                    kept_poly = max(gm, key=lambda h: len(h['poly']))['poly']
                    kept_polys[key] = kept_poly
                elif key.endswith('_obj'):
                    how, why = 'actor', 'a character: outlined live from the model'
            regions[key] = (how, why, reg, pt)
        # Where two objects claim the same pixels, each pixel goes to the nearer object point.
        owner = {}
        for key, (how, why, reg, pt) in regions.items():
            if how in ('depth', 'surface', 'carried') and reg:
                for p in reg:
                    d = (p[0] - pt[0]) ** 2 + (p[1] - pt[1]) ** 2
                    if p not in owner or d < owner[p][0]:
                        owner[p] = (d, key)
        for key, (how, why, reg, pt) in sorted(regions.items()):
            o = objs[st][key]
            if how in ('depth', 'surface', 'carried') and reg:
                reg = {p for p in reg if owner[p][1] == key}
            if how in ('carried', 'surface') and reg:
                reg = largest(reg)
            poly = (kept_polys.get(key) if how == 'kept' else
                    hull(reg) if how in ('carried', 'surface') else polygon(largest(reg))) if reg else None
            results.append({'set': st, 'setup': i, 'camera': su['name'], 'object': key, 'id': o['id'],
                            'name': o['name'], 'how': how, 'why': why, 'at': [round(pt[0]), round(pt[1])],
                            'area': len(reg) if reg else 0, 'poly': poly})
            col = {'depth': 'magenta', 'surface': 'deepskyblue', 'carried': 'lime', 'kept': 'yellow', 'actor': 'orange', 'flag': 'red'}[how]
            if poly:
                pts = ' '.join(f'{x},{y}' for x, y in poly)
                draw += ['-fill', 'none', '-stroke', col, '-strokewidth', '1', '-draw', f'polygon {pts}']
            x, y = int(pt[0]), int(pt[1])
            draw += ['-fill', col, '-stroke', 'black', '-draw', f'circle {x},{y} {x + 3},{y}',
                     '-stroke', 'none', '-pointsize', '11', '-draw', f'text {min(x + 5, 560)},{max(y - 5, 12)} "{o["name"][:22]}"']
        if out and draw and su['name'] in bgs:
            try:
                w, h, px = grimfiles.bitmap(game.read(bgs[su['name']]))
                ppm = os.path.join(out, f'{st}-{i}.ppm')
                open(ppm, 'wb').write(grimfiles.rgb565_ppm(w, h, px))
                subprocess.run(['magick', ppm] + (['-font', FONT] if FONT else []) + draw + [
                    '-gravity', 'NorthWest', '-fill', 'white', '-undercolor', '#000a', '-pointsize', '13',
                    '-annotate', '+4+4', f' {st} / {su["name"]} ', os.path.join(out, f'{st}-{i}-{su["name"]}.png')], check=True)
                os.remove(ppm)
            except Exception as e:
                print(f'{st} {su["name"]}: sheet failed: {e}')
    return results


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    game = grimfiles.Game(sys.argv[1])
    raw = os.path.join(ROOT, 'build', 'inventory', 'raw')
    objs = inv.objects(os.path.join(ROOT, 'build', 'inventory', 'lua'))
    report = json.load(open(os.path.join(ROOT, 'build', 'inventory', 'inventory.json')))
    out = os.path.join(ROOT, 'build', 'outlines')
    os.makedirs(out, exist_ok=True)
    sets = sys.argv[2:] or sorted(report)
    allr = []
    for st in sets:
        allr += run(game, st, raw, objs, report, out)
    json.dump(allr, open(os.path.join(out, 'outlines.json'), 'w'))
    c = collections.Counter(r['how'] for r in allr)
    print(f"{len(allr)} object views: depth {c['depth']}, surface {c['surface']}, carried {c['carried']}, kept {c['kept']}, actor {c['actor']}, flagged {c['flag']}")
    print('->', os.path.relpath(out))


if __name__ == '__main__':
    sys.exit(main())
