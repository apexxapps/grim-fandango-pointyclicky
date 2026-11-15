#!/usr/bin/env python3
"""trial.py <x> <y> <pre> <post>: <pre> timestamped shots, a tap at (x,y), <post> shots; onsets of each pump, the tap's time."""
import json, subprocess, sys
G = '/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/tools/proof/g.py'
B = '/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/bench/proof/burst/'
x, y, pre, post = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
delay = float(sys.argv[5]) if len(sys.argv) > 5 else None   # tap this long after pump1 (TL) strikes
steps = []
for i in range(pre + post):
    if i == pre:
        ref = sys.argv[6] if len(sys.argv) > 6 else "TL"
        RB = {"TL": ("22x14+454+113", 98, True), "BR": ("22x14+558+138", 140, False), "TR": ("22x14+556+113", 140, False)}[ref]
        tapst = {"click": [x, y]} if delay is None else {"onbeat": RB[0], "thr": RB[1], "below": RB[2], "delay": delay, "then": {"click": [x, y]}}
        steps += [{"stamp": 1}, tapst, {"stamp": 1}]
    steps += [{"stamp": 1}, {"shot": "proof/burst/t%02d" % i}]
out = subprocess.run(['python3', G, json.dumps(steps)], capture_output=True, text=True).stdout
lines = out.splitlines()
st = [float(l.split()[1]) for l in lines if l.startswith('stamp')]
for l in lines:
    if not l.startswith(('stamp', 'shot')):
        print(l)
tap = st[pre + 1]
st = st[:pre] + st[pre + 2:]
boxes = {'TL': '22x14+454+113', 'BL': '22x14+462+137', 'TR': '22x14+556+113', 'BR': '22x14+558+138'}
def hit(k, v):
    return {'TL': v < 98, 'BL': v > 83, 'TR': v > 140, 'BR': v > 140}[k]
n = pre + post
print('tap %.2f' % (tap % 100))
for k, g in boxes.items():
    vals = [float(subprocess.run(['magick', B + 't%02d.png' % i, '-crop', g, '+repage', '-colorspace', 'gray', '-format', '%[fx:mean*1000]', 'info:'], capture_output=True, text=True).stdout) for i in range(n)]
    on = [st[i] for i in range(n) if hit(k, vals[i]) and (i == 0 or not hit(k, vals[i - 1]))]
    print(k, ' '.join('%.2f' % (t % 100) for t in on))
