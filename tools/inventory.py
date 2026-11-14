#!/usr/bin/env python3
"""The game's own answer key: every object Grim Fandango defines, in every set
and every camera angle, checked against our hotspots.

    python3 -I tools/inventory.py <grim folder> <delua> [--out build/inventory]

<grim folder> is your own copy of the game (the folder with DATA000.LAB ...
DATA004.LAB); <delua> is scummvm-tools' Lua 3.1 decompiler. Nothing from the
game is written into this repository: the extracted scripts and the report
go to build/ (git-ignored).

What it reads:
  - every set's Lua (decompiled): `Object:create(set, "/id/name", x, y, z,
    { range = r })`, the object's handlers (lookAt, use, pickUp, walkOut ...)
    and whether a script ever makes it (un)touchable;
  - every set file (.set): each camera setup's position, interest, roll and
    field of view.
Each object's world position is projected onto each setup with the same
maths as the engine (HotspotMan::worldToScreen) and compared with
data/hotspots/<set>.set.hot, whose polygons are linked to objects by id.

Findings, per set and setup:
  missing   the object is on screen here and nothing of ours points at it
  off       a hotspot names the object, but the object's own point falls
            outside the polygon (how far, in game pixels)
  stray     a hotspot names an id the set's scripts never create
Objects created at 0,0,0 with range 0 are inventory or script-only things
(not in the room), and are listed apart.
"""
import json
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grimfiles  # noqa: E402
import os
import re
import struct
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W, H = 640, 480


# MARK: The game's files

def extract(game, out):
    """Every .lua and .set from the game's DATA LABs into out/."""
    os.makedirs(out, exist_ok=True)
    for lab in sorted(f for f in os.listdir(game) if re.match(r'(?i)data\d+\.lab$', f)):
        d = open(os.path.join(game, lab), 'rb').read()
        if d[:4] != b'LABN':
            continue
        _, n, nl = struct.unpack('<III', d[4:16])
        names = d[16 + 16 * n:16 + 16 * n + nl]
        for i in range(n):
            no, off, size, _ = struct.unpack('<IIII', d[16 + 16 * i:32 + 16 * i])
            name = names[no:names.index(b'\0', no)].decode('latin-1')
            if name.lower().endswith(('.lua', '.set')):
                with open(os.path.join(out, name.lower()), 'wb') as f:
                    f.write(d[off:off + size])


def decompile(raw, delua, out):
    os.makedirs(out, exist_ok=True)
    for name in sorted(os.listdir(raw)):
        if name.endswith('.lua'):
            dst = os.path.join(out, name)
            if not os.path.exists(dst):
                r = subprocess.run([delua, os.path.join(raw, name)], capture_output=True, text=True, errors='replace')
                with open(dst, 'w') as f:
                    f.write(r.stdout)


# MARK: Sets and objects

def setups(path):
    """A set file's camera setups, in order (the order hotspots number them)."""
    out, cur = [], None
    for line in open(path, encoding='latin-1'):
        tok = line.split()
        if not tok:
            continue
        if tok[0] == 'section:' and out and tok[1] != 'setups':
            break
        if tok[0] == 'setup':
            cur = {'name': tok[1]}
            out.append(cur)
        elif cur is not None and tok[0] in ('position', 'interest'):
            cur[tok[0]] = [float(t) for t in tok[1:4]]
        elif cur is not None and tok[0] in ('roll', 'fov'):
            cur[tok[0]] = float(tok[1])
        elif cur is not None and tok[0] == 'zbuffer':
            cur['zbuffer'] = tok[1]
    return [s for s in out if 'position' in s and 'interest' in s and 'fov' in s]


def camera_sectors(path):
    """The names of a set's camera sectors: standing in one shows its setup."""
    names, cur = set(), None
    for line in open(path, encoding='latin-1'):
        tok = line.split()
        if len(tok) >= 2 and tok[0] == 'sector':
            cur = tok[1]
        elif len(tok) >= 2 and tok[0] == 'type' and tok[1] == 'camera' and cur:
            names.add(cur)
    return names


def in_play(setup, cams):
    """A setup the player walks around in: a camera sector is named after it
    (mo_ddtws, mo_ddtws2 -> mo_ddtws). The rest are cut-scene and close-up angles."""
    n = setup['name'].lower()
    return any(c.lower() == n or (c.lower().startswith(n) and c[len(n):].isdigit()) for c in cams)


NUM = r'(-?[\d.]+(?:e-?\d+)?)'
CREATE = re.compile(r'^(\w+)\.(\w+)\s*=\s*Object:create\((\w+),\s*"(/\w+/)?([^"]*)",\s*' + NUM + r',\s*' + NUM + r',\s*' + NUM + r'(?:,\s*\{[^}]*range\s*=\s*' + NUM + r')?')
HANDLER = re.compile(r'^(\w+)\.(\w+)\.(lookAt|use|pickUp|walkOut|use_(?!pnt_|rot_)\w+|default_response)\s*=')
TOUCH = re.compile(r'(\w+)\.(\w+):make_(un)?touchable\(')


def objects(dec_dir):
    """{set: {key: object}} from every decompiled script."""
    sets = {}
    handlers, touch = {}, {}
    for name in sorted(os.listdir(dec_dir)):
        for line in open(os.path.join(dec_dir, name), encoding='latin-1'):
            line = line.strip()
            m = CREATE.match(line)
            if m:
                st, key, owner, oid, oname, x, y, z, rng = m.groups()
                sets.setdefault(owner, {})[key] = {
                    'key': key, 'id': (oid or '').strip('/'), 'name': oname,
                    'pos': [float(x), float(y), float(z)], 'range': float(rng or 0),
                    'script': name, 'handlers': set(), 'touchable': set()}
                continue
            m = HANDLER.match(line)
            if m:
                handlers.setdefault((m.group(1), m.group(2)), set()).add(m.group(3))
            for m in TOUCH.finditer(line):
                touch.setdefault((m.group(1), m.group(2)), set()).add('off' if m.group(3) else 'on')
    for st, objs in sets.items():
        for key, o in objs.items():
            o['handlers'] = sorted(handlers.get((st, key), ()))
            o['touchable'] = sorted(touch.get((st, key), ()))
    return sets


# MARK: The engine's projection (HotspotMan::worldToScreen)

def sub(a, b): return [a[i] - b[i] for i in range(3)]
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def norm(a):
    l = math.sqrt(dot(a, a)) or 1.0
    return [v / l for v in a]


def project(setup, p):
    pos, interest = setup['position'], setup['interest']
    up = [0, 1, 0] if (pos[0] == interest[0] and pos[1] == interest[1]) else [0, 0, 1]
    f = norm(sub(interest, pos))
    s = norm(cross(f, up))
    u = cross(s, f)
    tan_x = math.tan(setup['fov'] / 2 * math.pi / 180)
    roll = math.radians(setup.get('roll', 0.0))
    d = sub(p, pos)
    ex, ey, depth = dot(s, d), dot(u, d), dot(f, d)
    if depth <= 0:
        return None
    rx = math.cos(roll) * ex + math.sin(roll) * ey
    ry = -math.sin(roll) * ex + math.cos(roll) * ey
    x = (rx / depth / tan_x + 1) * 0.5 * W
    y = H - (ry / depth / (0.75 * tan_x) + 1) * 0.5 * H
    return (x, y) if 0 <= x < W and 0 <= y < H else None


# MARK: Our hotspots

def hotspots(path):
    out = []
    if not os.path.exists(path):
        return out
    for line in open(path, encoding='latin-1'):
        line = line.strip()
        if not line:
            continue
        start, _, rest = line.partition('"')
        desc, _, end = rest.partition('"')
        setup, _, hid = start.strip().partition(' ')
        tok = end.split()
        htype, npos = int(tok[0]), int(tok[1])
        npts = int(tok[2 + npos * 3])
        poly = [int(t) for t in tok[3 + npos * 3:3 + npos * 3 + npts * 2]]
        out.append({'setup': int(setup), 'id': hid.strip('/'), 'name': desc, 'type': htype,
                    'poly': list(zip(poly[::2], poly[1::2]))})
    return out


def inside(pt, poly):
    x, y, c = pt[0], pt[1], False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-9) + x1:
            c = not c
    return c


def distance(pt, poly):
    if inside(pt, poly):
        return 0.0
    best = 1e9
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        dx, dy = x2 - x1, y2 - y1
        t = max(0, min(1, ((pt[0] - x1) * dx + (pt[1] - y1) * dy) / ((dx * dx + dy * dy) or 1)))
        best = min(best, math.hypot(pt[0] - x1 - t * dx, pt[1] - y1 - t * dy))
    return best


# MARK: The audit

def hidden(game, setup, p, pt, cache={}):
    """True when the angle's depth image puts something in front of the
    object's point (checked over a 9x9 pixel patch: thin things count)."""
    name = setup.get('zbuffer')
    if not name or not game:
        return False
    if name not in cache:
        try:
            cache[name] = grimfiles.bitmap(game.read(name))
        except Exception:
            cache[name] = None
    if not cache[name]:
        return False
    w, h, z = cache[name]
    f = norm(sub(setup['interest'], setup['position']))
    d = dot(f, sub(p, setup['position']))
    tol = max(0.3, 0.15 * d)
    for dy in range(-4, 5, 2):
        for dx in range(-4, 5, 2):
            x, y = int(pt[0]) + dx, int(pt[1]) + dy
            if 0 <= x < w and 0 <= y < h and grimfiles.zdepth(z[y * w + x]) >= d - tol:
                return False
    return True


def audit(raw, dec, game=None):
    objs = objects(dec)
    report = {}
    for name in sorted(os.listdir(raw)):
        if not name.endswith('.set'):
            continue
        st = name[:-4]
        sus = setups(os.path.join(raw, name))
        cams = camera_sectors(os.path.join(raw, name))
        ours = hotspots(os.path.join(ROOT, 'data', 'hotspots', st + '.set.hot'))
        mine = objs.get(st, {})
        placed = {k: o for k, o in mine.items() if not (o['pos'] == [0, 0, 0] and o['range'] == 0)}
        ids = {o['id'] for o in mine.values() if o['id']}
        play = [i for i, su in enumerate(sus) if in_play(su, cams)]
        r = {'setups': len(sus), 'play': [sus[i]['name'] for i in play], 'objects': len(placed), 'offstage': sorted(k for k in mine if k not in placed),
             'hotspots': len(ours), 'missing': [], 'off': [], 'stray': []}
        for i, su in enumerate(sus):
            if i not in play:
                continue
            here = [h for h in ours if h['setup'] == i]
            for key, o in sorted(placed.items()):
                pt = project(su, o['pos'])
                if not pt:
                    continue
                if hidden(game, su, o['pos'], pt):
                    r.setdefault('hidden', []).append({'setup': i, 'object': key})
                    continue
                mine_h = [h for h in here if h['id'] == o['id']] if o['id'] else []
                if not mine_h:
                    r['missing'].append({'setup': i, 'camera': su['name'], 'object': key, 'name': o['name'],
                                         'id': o['id'], 'at': [round(pt[0]), round(pt[1])], 'does': o['handlers'],
                                         'touchable': o['touchable']})
                else:
                    d = min(distance(pt, h['poly']) for h in mine_h)
                    if d > 0:
                        r['off'].append({'setup': i, 'camera': su['name'], 'object': key, 'name': o['name'],
                                         'id': o['id'], 'at': [round(pt[0]), round(pt[1])], 'by': round(d)})
            for h in here:
                if h['type'] in (1, 2) and h['id'] not in ids and not h['id'].startswith('to'):
                    r['stray'].append({'setup': i, 'id': h['id'], 'name': h['name']})
        report[st] = r
    return report


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 2:
        sys.exit(__doc__)
    game, delua = args
    out = os.path.join(ROOT, 'build', 'inventory')
    raw, dec = os.path.join(out, 'raw'), os.path.join(out, 'lua')
    extract(game, raw)
    decompile(raw, delua, dec)
    report = audit(raw, dec, grimfiles.Game(game))
    json.dump(report, open(os.path.join(out, 'inventory.json'), 'w'), indent=1)
    tot = {k: sum(len(r[k]) if isinstance(r[k], list) else r[k] for r in report.values())
           for k in ('objects', 'hotspots', 'missing', 'off', 'stray')}
    nohs = sorted(s for s, r in report.items() if r['hotspots'] == 0 and r['objects'])
    print(f"{len(report)} sets: {tot['objects']} objects placed in the world, {tot['hotspots']} hotspots")
    print(f"missing {tot['missing']} (object on screen, no hotspot) · off {tot['off']} (point outside its polygon) · stray {tot['stray']}")
    print('sets with objects and no hotspots at all:', ' '.join(nohs) or 'none')
    print('->', os.path.relpath(os.path.join(out, 'inventory.json')))


if __name__ == '__main__':
    sys.exit(main())
