#!/usr/bin/env python3
"""observe.py <name> <patch.lua|-> <steps.json> [--load N] : a separate developer-mode run (BENCH_DEVEL=1),
never the proof game: boots, loads slot N, runs <patch.lua> with Ctrl+P (the lab dir's 'patch'), then the steps."""
import json, subprocess, sys, os
R = '/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky'
W = R + '/build/proof-bench'
G = "/Users/simonstark/Library/Developer/CoreSimulator/Devices/28091D11-A25F-4C5D-B4C3-E0773C1C3E78/data/Containers/Data/Application/2AB2B466-7AB0-4BE8-85A0-98264DF04E6E/Documents/Grim Fandango/Game"
name, patch, steps = sys.argv[1:4]
load = int(sys.argv[sys.argv.index('--load') + 1]) if '--load' in sys.argv else None
if patch != '-':
    open(W + '/labs/patch', 'w').write(open(patch).read())
boot = [{"wait": 5}, {"key": "esc"}, {"wait": 3}, {"key": "esc"}, {"wait": 3}, {"key": "esc"}, {"wait": 6}]
if load is not None:
    boot += [{"load": load}, {"wait": float(os.environ.get("OBS_WAIT", "1.5"))}]
if patch != '-':
    boot += [{"key": "ctrl"}, {"key": "p"}, {"wait": 5}]
s = json.load(open(steps))
for st in s:
    if 'shot' in st:
        st['shot'] = name + '-' + st['shot']
json.dump(boot + s, open(W + '/s/_run.json', 'w'))
subprocess.run(['python3', '-I', R + '/tools/bench.py', G, os.path.expanduser('~/Developer/pointyclicky-build/grim-bench/scummvm'),
                W + '/labs', W + '/s/_run.json'], env=dict(os.environ, BENCH_DEVEL='1'), stdout=subprocess.DEVNULL)
for l in open(R + '/build/bench/scummvm.out', errors='replace').read().splitlines():
    if 'Grim Mouse: ' in l and 'sets with' not in l or 'rror' in l or 'Executing sentence' in l or 'say_line' in l or 'Debug: Q' in l:
        print(l[:300])
