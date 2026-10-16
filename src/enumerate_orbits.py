#!/usr/bin/env python3
"""Exhaustively enumerate cyclic triple / 5-set orbits over Z/31 using exact integers."""
import itertools as it, json, pathlib, hashlib
from collections import Counter
P = pathlib.Path(__file__).resolve().parents[1]
N=31

def canon(a):
    a=tuple(a)
    return min(tuple(sorted((x-y)%N for x in a)) for y in a)

def pair_distances(b):
    a=[0]*15
    for x,y in it.combinations(b,2):
        d=(x-y)%N
        a[min(d,N-d)-1]+=1
    return a

def main():
    import time
    start=time.perf_counter()
    triples=sorted({canon((0,x,y)) for x,y in it.combinations(range(1,N),2)})
    rid={t:i for i,t in enumerate(triples)}
    print('triple orbits', len(triples), flush=True)
    candidates=[]; num_orbits=0; invalid=0
    for x in it.combinations(range(1,N),4):
        b=(0,)+x
        if canon(b)!=b: continue
        num_orbits+=1
        rr=[rid[canon(t)] for t in it.combinations(b,3)]
        if len(set(rr))<10:
            invalid+=1
            continue
        candidates.append({'block':list(b), 'resources': sorted(rr), 'distance_loads': pair_distances(b)})
    assert len(triples)==145 and num_orbits==5481 and len(candidates)==4761, (num_orbits, len(candidates),invalid)
    assert all(sum(c['distance_loads'])==10 for c in candidates)
    print('5-set orbits',num_orbits,'internally valid',len(candidates),'invalid',invalid)
    (P/'data'/'triples.json').write_text(json.dumps(triples, separators=(',',':'))+'\n')
    (P/'data'/'orbit_candidates.json').write_text(json.dumps(candidates, separators=(',',':'))+'\n')
    # compact matrix only
    (P/'data'/'resource_matrix.json').write_text(json.dumps([x['resources'] for x in candidates], separators=(',',':'))+'\n')
    data='\n'.join(','.join(map(str,x['block']))+'|'+','.join(map(str,x['resources'])) for x in candidates)+'\n'
    (P/'data'/'candidates.tsv').write_text(data)
    digest=hashlib.sha256(data.encode()).hexdigest()
    print('mapping sha256',digest,'elapsed',round(time.perf_counter()-start,2),'seconds')
    # symmetry orbits under multipliers 1..30: build orbit partition
    byblock={tuple(c['block']):i for i,c in enumerate(candidates)}
    mult=[]; visited=set()
    for i,c in enumerate(candidates):
        if i in visited:continue
        orbit=sorted({byblock[canon(((a*x)%N for x in c['block']))] for a in range(1,N)})
        visited.update(orbit)
        mult.append(orbit)
    assert sum(len(g) for g in mult)==len(candidates)
    (P/'data'/'multiplier_orbits.json').write_text(json.dumps(mult,separators=(',',':'))+'\n')
    print('multiplier classes',len(mult),'sizes',dict(sorted(Counter(map(len,mult)).items())))
if __name__=='__main__':main()
