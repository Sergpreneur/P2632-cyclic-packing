#!/usr/bin/env python3
"""Write a fully specified CNF for M >= k using Sinz AMO + unary cardinality.
Each of the 145 triple-orbit resources has an at-most-one sequential ladder.
The at-least-k cardinality bound is encoded with a binary Tseitin recursion
  s[i,j] <-> (s[i-1,j] or (x[i] and s[i-1,j-1])).
No solver is required to generate CNF. This file is not an UNSAT certificate.
"""
import pathlib,json,argparse
P=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--target',type=int,default=13)
parser.add_argument('--output',type=pathlib.Path,default=P/'certificates/unsat/target_13.cnf')
args=parser.parse_args()
D=json.loads((P/'data/orbit_candidates.json').read_text())
N=len(D); k=args.target
assert 1<=k<=14
rows=[[] for _ in range(145)]
for i,d in enumerate(D):
  for r in d['resources']:rows[r].append(i+1)
nextvar=N
clauses=[]
def new():
  global nextvar
  nextvar+=1
  return nextvar

def neg(x):
  if x is True:return False
  if x is False:return True
  return -x

def add(*items):
  if any(item is True for item in items):return
  v=[]
  for a in items:
    if a is False:continue
    v.append(a)
  if not v:raise RuntimeError('unsatisfiable clause generated')
  clauses.append(tuple(v))

for row in rows:
  if len(row)<=1:continue
  s=new();add(-row[0],s)
  for i in range(1,len(row)-1):
    t=new()
    add(-row[i],t)
    add(-s,t)
    add(-row[i],-s)
    s=t
  add(-row[-1],-s)
# unary exact count of selected rows, truncated to k
prev={0:True}
for i,x in enumerate(range(1,N+1),start=1):
  curr={0:True}
  for j in range(1,min(k,i)+1):
    a=prev.get(j,False)
    b=prev.get(j-1,False)
    z=new()
    # z <-> (a or (x and b))
    add(neg(a),z)
    add(-x,neg(b),z)
    add(-z,a,x)
    add(-z,a,b)
    curr[j]=z
  prev=curr
add(prev[k])
args.output.parent.mkdir(parents=True,exist_ok=True)
with args.output.open('w') as f:
  f.write(f'c P2632 exactly encoded: 4761 block vars, 145 resource AMO, at least {k} blocks\n')
  f.write(f'p cnf {nextvar} {len(clauses)}\n')
  for clause in clauses:f.write(' '.join(map(str,clause))+' 0\n')
print('Created',args.output,'vars',nextvar,'clauses',len(clauses),'size',args.output.stat().st_size)
