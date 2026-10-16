#!/usr/bin/env python3
"""Integer Johnson-type upper bound; verify that each distance is loaded <= 9."""
import json,itertools, pathlib
from math import comb
P=pathlib.Path(__file__).resolve().parents[1]
D=json.loads((P/'data/best_packing.json').read_text())
assert comb(31,3)==4495
assert 145==comb(31,3)//31
assert 5481==comb(31,5)//31
assert 418==9*comb(31,2)//comb(5,2)
assert 13==418//31
loads=[0]*15
for B in D['blocks']:
    for x,y in itertools.combinations(B,2):
        d=(x-y)%31
        loads[min(d,31-d)-1]+=1
assert max(loads)<=9
assert sum(loads)==10*len(D['blocks'])
print('known upper M<=13; proved via pair incidence; current constructive lower',len(D['blocks']))
print('distance 1..15 loads:', loads)
print('deficits 9-load:',[9-x for x in loads])
