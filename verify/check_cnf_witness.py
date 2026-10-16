#!/usr/bin/env python3
"""Validate an encoded DIMACS witness for a construction, including all auxiliary variables.
For k > witness size, the final cardinality clause is expected to fail, nothing more.
This is a CNF consistency test, not a proof of UNSAT.
"""
import argparse,json,pathlib
p=argparse.ArgumentParser();p.add_argument('cnf');p.add_argument('--target',type=int,required=True)
a=p.parse_args()
P=pathlib.Path(__file__).resolve().parents[1]
D=json.loads((P/'data/orbit_candidates.json').read_text())
B=json.loads((P/'data/best_packing.json').read_text())['blocks']
lookup={tuple(d['block']):i+1 for i,d in enumerate(D)}
chosen={lookup[tuple(b)] for b in B}
N=len(D)
truth={i:(i in chosen) for i in range(1,N+1)}
R=[[] for _ in range(145)]
for i,d in enumerate(D,1):
    for r in d['resources']:R[r].append(i)
last=N
for row in R:
    if len(row)<=1:continue
    last+=1;truth[last]=truth[row[0]]
    for j in range(1,len(row)-1):
        last+=1
        truth[last]=truth[last-1] or truth[row[j]]
count=0
for i in range(1,N+1):
    count+=i in chosen
    for j in range(1,min(a.target,i)+1):
        last+=1
        truth[last]=(count>=j)
wrong=[]
with open(a.cnf) as f:
    for line in f:
        if line[0] in ('c','p'):continue
        lits=list(map(int,line.split()))
        assert lits[-1]==0
        if not any(truth[abs(x)] == (x>0) for x in lits[:-1]):
            wrong.append(lits[:-1])
print('M=',len(B),'target=',a.target,'vars_checked=',last,'violated_CNF_clauses=',len(wrong))
if len(B)>=a.target:
    assert not wrong,wrong[:3]
else:
    assert len(wrong)==1,wrong[:3]
print('PASS: witness matches DIMACS encoding semantics')
