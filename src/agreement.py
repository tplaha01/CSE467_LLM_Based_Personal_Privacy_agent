import csv
from . import HARMS
def agreement(path_a,path_b):
    def read(p):
        with open(p,encoding="utf-8",newline="") as f: return {r["statement_id"]:r for r in csv.DictReader(f)}
    a,b=read(path_a),read(path_b); out={}
    for h in HARMS:
        pairs=[(int(a[i][h]),int(b[i][h])) for i in a.keys() & b.keys()]; n=len(pairs); agree=sum(x==y for x,y in pairs)/n if n else 0
        pa=sum(x for x,y in pairs)/n if n else 0; pb=sum(y for x,y in pairs)/n if n else 0; pe=pa*pb+(1-pa)*(1-pb)
        out[h]={"raw_agreement":agree,"cohens_kappa":(agree-pe)/(1-pe) if pe != 1 else 1.0}
    return out
