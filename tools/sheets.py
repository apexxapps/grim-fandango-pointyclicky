#!/usr/bin/env python3
"""Contact sheets: one picture per camera angle you play in, showing the game's
truth and ours over the real background.

    python3 -I tools/sheets.py <grim folder> [set ...]     # after inventory.py

Writes build/sheets/<set>-<setup>.png (git-ignored: they contain the game's
art). On each:
  green dot + name   an object the game's scripts place here, and our hotspot covers it
  red dot + name     an object on screen with nothing of ours pointing at it (missing)
  amber dot          our hotspot names it, but its point is outside the outline (off)
  grey dot           the depth image hides it at this angle
  yellow outline     our hotspot (object); cyan: exit / walk path; magenta: other
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grimfiles  # noqa: E402
import inventory as inv  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
COLOURS = {1: 'yellow', 2: 'cyan', 3: 'cyan'}
FONT = next((f for f in ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc',
                          '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') if os.path.exists(f)), None)


def sheet(game, st, raw, objs, report, out):
    sus = inv.setups(os.path.join(raw, st + '.set'))
    cams = inv.camera_sectors(os.path.join(raw, st + '.set'))
    bgs, cur = {}, None
    for line in open(os.path.join(raw, st + '.set'), encoding='latin-1'):
        t = line.split()
        if t[:1] == ['setup']:
            cur = t[1]
        elif t[:1] == ['background'] and cur:
            bgs[cur] = t[1]
    ours = inv.hotspots(os.path.join(ROOT, 'data', 'hotspots', st + '.set.hot'))
    r = report.get(st, {})
    made = []
    for i, su in enumerate(sus):
        if not inv.in_play(su, cams) or su['name'] not in bgs:
            continue
        try:
            w, h, px = grimfiles.bitmap(game.read(bgs[su['name']]))
        except Exception as e:
            print(f'{st} {su["name"]}: {e}')
            continue
        ppm = os.path.join(out, f'{st}-{i}.ppm')
        open(ppm, 'wb').write(grimfiles.rgb565_ppm(w, h, px))
        draw = []
        for hs in ours:
            if hs['setup'] != i or len(hs['poly']) < 3:
                continue
            col = COLOURS.get(hs['type'], 'magenta')
            pts = ' '.join(f'{x},{y}' for x, y in hs['poly'])
            draw += ['-fill', 'none', '-stroke', col, '-strokewidth', '1', '-draw', f'polygon {pts}']
        missing = {m['object'] for m in r.get('missing', []) if m['setup'] == i}
        off = {m['object'] for m in r.get('off', []) if m['setup'] == i}
        hid = {m['object'] for m in r.get('hidden', []) if m['setup'] == i}
        for key, o in sorted(objs.get(st, {}).items()):
            if o['pos'] == [0, 0, 0] and o['range'] == 0:
                continue
            pt = inv.project(su, o['pos'])
            if not pt:
                continue
            col = 'red' if key in missing else 'orange' if key in off else 'grey60' if key in hid else 'lime'
            x, y = int(pt[0]), int(pt[1])
            draw += ['-fill', col, '-stroke', 'black', '-strokewidth', '1',
                     '-draw', f'circle {x},{y} {x + 4},{y}',
                     '-stroke', 'none', '-fill', col, '-pointsize', '11',
                     '-draw', f'text {min(x + 6, 560)},{max(y - 6, 12)} "{o["name"][:24]}"']
        png = os.path.join(out, f'{st}-{i}-{su["name"]}.png')
        subprocess.run(['magick', ppm] + (['-font', FONT] if FONT else []) + draw + [
            '-gravity', 'NorthWest', '-fill', 'white', '-undercolor', '#000a', '-pointsize', '13',
            '-annotate', '+4+4', f' {st} / {su["name"]} (setup {i}) ', png], check=True)
        os.remove(ppm)
        made.append(png)
    return made


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    game = grimfiles.Game(sys.argv[1])
    raw = os.path.join(ROOT, 'build', 'inventory', 'raw')
    objs = inv.objects(os.path.join(ROOT, 'build', 'inventory', 'lua'))
    report = json.load(open(os.path.join(ROOT, 'build', 'inventory', 'inventory.json')))
    out = os.path.join(ROOT, 'build', 'sheets')
    os.makedirs(out, exist_ok=True)
    sets = sys.argv[2:] or sorted(report)
    n = 0
    for st in sets:
        n += len(sheet(game, st, raw, objs, report, out))
    print(f'{n} sheets -> {os.path.relpath(out)}')


if __name__ == '__main__':
    sys.exit(main())
