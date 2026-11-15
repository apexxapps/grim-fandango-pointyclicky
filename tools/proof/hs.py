#!/usr/bin/env python3
import sys,shlex
R='/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/data/hotspots/'
s=sys.argv[1]; su=sys.argv[2] if len(sys.argv)>2 else None
for line in open(R+s+'.set.hot'):
    p=shlex.split(line)
    if not p: continue
    setup,id_,name,typ,npos=p[0],p[1],p[2],p[3],int(p[4])
    rest=p[5+3*npos:]
    n=int(rest[0]); pts=list(map(int,rest[1:1+2*n]))
    xs,ys=pts[0::2],pts[1::2]
    if su is not None and setup!=su: continue
    print(setup,id_,repr(name),'type',typ,'c=(%d,%d)'%(sum(xs)/n,sum(ys)/n),'box',min(xs),min(ys),max(xs),max(ys))
