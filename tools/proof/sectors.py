import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); G = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "daemon.py")).read().split("G = \"")[1].split("\"")[0]
import grimfiles
# sectors.py <set> <x0> <x1> <y0> <y1> : the set file's sectors (name, type, visibility, corners) that meet the box; run with python3 -I
s,x0,x1,y0,y1=sys.argv[1],*map(float,sys.argv[2:6])
d=grimfiles.Game(G).read(s+'.set').decode('latin1')
for blk in d.split('sector')[1:]:
    L=[l.strip() for l in blk.split('\n')]
    name=L[0].split()[0] if L[0] else '?'
    typ=vis='';v=[]
    on=False
    for l in L:
        if l.startswith('type'): typ=l.split()[1]
        if l.startswith('default visibility'): vis=l.split()[-1]
        if l.startswith('vertices:'): on=True; l=l[9:].strip()
        if on:
            p=l.split()
            if len(p)==3:
                try: v.append(tuple(map(float,p)))
                except: on=False
            elif l=='' and v: on=False
    if not v: continue
    xs=[a[0] for a in v]; ys=[a[1] for a in v]
    if min(xs)<x1 and max(xs)>x0 and min(ys)<y1 and max(ys)>y0:
        print(name,typ,vis,[(round(a[0],3),round(a[1],3)) for a in v])
