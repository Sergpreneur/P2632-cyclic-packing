#!/usr/bin/env python3
"""Independently reconstruct orbit partition under nonzero multipliers of F_31."""
import json,pathlib,collections,itertools
P=pathlib.Path(__file__).resolve().parents[1]
D=json.loads((P/'data/orbit_candidates.json').read_text())
blocks=[tuple(e['block']) for e in D]
byblock={t:i for i,t in enumerate(blocks)}

def canon(a):
    a=tuple(a)
    return min(tuple(sorted((v-x)%31 for v in a)) for x in a)
visited=set();classes=[]
for i,b in enumerate(blocks):
    if i in visited:continue
    orbit=sorted({byblock[canon(a*x%31 for x in b)] for a in range(1,31)})
    assert i in orbit
    visited.update(orbit)
    classes.append(orbit)
assert len(visited)==len(D)==4761
assert len(classes)==162
sizehist=dict(sorted(collections.Counter(map(len,classes)).items()))
print('multiplier orbits=',len(classes),'histogram=',sizehist)
prior=json.loads((P/'data/multiplier_orbits.json').read_text())
assert prior==classes
print('OK: symmetry orbits match candidate enumeration')
