import sys
sys.path.insert(0,'/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/tools')
import inventory as inv
R='/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/inventory/raw/'
def P(st, su, pts):
    s=inv.setups(R+st+'.set')[su]
    out=[]
    for p in pts:
        q=inv.project(s,p)
        out.append(tuple(int(v) for v in q) if q else None)
    return out
if __name__=='__main__':
    st,su=sys.argv[1],int(sys.argv[2])
    pts=[tuple(map(float,a.split(','))) for a in sys.argv[3:]]
    for p,q in zip(pts,P(st,su,pts)): print(p,q)
