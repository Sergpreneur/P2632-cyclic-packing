#!/usr/bin/env python3
"""Exact 0-1 set packing model implemented using SciPy/HiGHS."""
import json, numpy as np, sys, time
from pathlib import Path
from scipy import sparse
from scipy.optimize import milp, LinearConstraint, Bounds
P=Path(__file__).resolve().parents[1]
data=json.loads((P/'data/orbit_candidates.json').read_text())
N=len(data); nrows=160
r=[];c=[];v=[]
for j,item in enumerate(data):
    for rr in item['resources']:
        r.append(rr); c.append(j); v.append(1)
    for d,count in enumerate(item['distance_loads']):
        if count:
            r.append(145+d);c.append(j);v.append(count)
A=sparse.coo_matrix((v,(r,c)),shape=(nrows,N)).tocsr()
U=np.array([1]*145+[9]*15)
objective=np.ones(N)*-1
opts={'time_limit': float(sys.argv[1]) if len(sys.argv)>1 else 30, 'disp':True,'mip_rel_gap':0.0}
print('MILP: nvars',N,'nrows',nrows,'nnz',A.nnz, 'options',opts,flush=True)
start=time.time()
res=milp(objective,integrality=np.ones(N),bounds=Bounds(0,1),constraints=LinearConstraint(A,0,U),options=opts)
print('Elapsed',time.time()-start,'status',res.status,'msg',res.message,'primal',res.fun,'mip_gap',res.mip_gap,'dual',res.mip_dual_bound,flush=True)
if res.x is not None:
    ids=np.flatnonzero(res.x>.5).tolist()
    print('solution',len(ids), ids,flush=True)
    if len(ids)>=10:
        out={'blocks':[data[i]['block'] for i in ids], 'candidate_indices':ids,'method':'SciPy milp HiGHS','objective':len(ids)}
        (P/'experiments/checkpoints/milp_best.json').write_text(json.dumps(out,indent=2)+'\n')
