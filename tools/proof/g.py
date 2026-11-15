#!/usr/bin/env python3
"""g.py '<json steps>'  or  g.py -f file.json ; prints the bench's lines and the new log lines"""
import json, socket, sys, os
LOG='/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/bench/scummvm.out'
POS='/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/proof-bench/.logpos'
arg = open(sys.argv[2]).read() if sys.argv[1]=='-f' else sys.argv[1]
steps = json.loads(arg)
s = socket.create_connection(('127.0.0.1', 47123))
s.sendall((json.dumps(steps)+'\n').encode())
d=b''
while True:
    c=s.recv(65536)
    if not c: break
    d+=c
lines=[l for l in d.decode().splitlines() if l and not l.startswith(("move {", "click {", "button {"))]
print('\n'.join(lines))
pos=int(open(POS).read()) if os.path.exists(POS) else 0
data=open(LOG,errors='replace').read()
if pos>len(data): pos=0
new=data[pos:]
open(POS,'w').write(str(len(data)))
keep=[l for l in new.splitlines() if l.strip() and ('Grim Mouse' in l or 'rror' in l or 'ssert' in l or 'WARNING' in l)]
print('\n'.join(keep[-25:]))
