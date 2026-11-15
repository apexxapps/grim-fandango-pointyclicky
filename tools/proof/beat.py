#!/usr/bin/env python3
"""beat.py [n] [pre-steps json]: n timestamped shots; each pump's strike onsets (wall clock).
Pumps: TL=pump1 (hose box4), BL=pump2 (box3), TR=pump3 (box2), BR=pump4 (box1)."""
import json, subprocess, sys
G = '/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/tools/proof/g.py'
B = '/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/bench/proof/burst/'
n = int(sys.argv[1]) if len(sys.argv) > 1 else 24
pre = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
steps = pre[:]
for i in range(n):
    steps += [{"stamp": 1}, {"shot": "proof/burst/e%02d" % i}]
out = subprocess.run(['python3', G, json.dumps(steps)], capture_output=True, text=True).stdout
lines = out.splitlines()
st = [float(l.split()[1]) for l in lines if l.startswith('stamp')]
for l in lines:
    if not l.startswith(('stamp', 'shot')):
        print(l)
st = st[len(st) - n:]
boxes = {'TL': '22x14+454+113', 'BL': '22x14+462+137', 'TR': '22x14+556+113', 'BR': '22x14+558+138'}
vals = {k: [] for k in boxes}
for i in range(n):
    for k, g in boxes.items():
        v = subprocess.run(['magick', B + 'e%02d.png' % i, '-crop', g, '+repage', '-colorspace', 'gray', '-format', '%[fx:mean*1000]', 'info:'], capture_output=True, text=True).stdout
        vals[k].append(float(v))
def hit(k, v):
    return {'TL': v < 98, 'BL': v > 83, 'TR': v > 140, 'BR': v > 140}[k]
res = {}
for k in boxes:
    on = [st[i] for i in range(n) if hit(k, vals[k][i]) and (i == 0 or not hit(k, vals[k][i - 1]))]
    res[k] = on
    print(k, ' '.join('%.2f' % (t % 100) for t in on), '   vals', ' '.join('%d' % v for v in vals[k]))
json.dump({'stamps': st, 'onsets': res}, open('/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/proof-bench/beat.json', 'w'))
