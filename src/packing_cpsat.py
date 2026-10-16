#!/usr/bin/env python3
"""Optional OR-Tools CP-SAT exact model. Requires: python -m pip install ortools."""
import argparse,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--target',type=int,default=13);p.add_argument('--seconds',type=float,default=120);p.add_argument('--seed',type=int,default=1)
a=p.parse_args()
try:
    from ortools.sat.python import cp_model
except ModuleNotFoundError:
    sys.exit('OR-Tools is not installed in this environment. This script is ready to run after installing ortools, but no CP-SAT claim is made.')
D=json.loads((P/'data/orbit_candidates.json').read_text())
model=cp_model.CpModel()
x=[model.NewBoolVar('B%d'%i) for i in range(len(D))]
R=[[] for _ in range(145)]
for i,c in enumerate(D):
    for r in c['resources']:R[r].append(x[i])
for r in R:model.Add(sum(r)<=1)
for d in range(15):model.Add(sum(c['distance_loads'][d]*x[i] for i,c in enumerate(D))<=9)
model.Add(sum(x)>=a.target)
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=a.seconds
solver.parameters.random_seed=a.seed
solver.parameters.num_search_workers=4
status=solver.Solve(model)
print('status=',solver.StatusName(status),'wall_time=',solver.WallTime())
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    ids=[i for i,y in enumerate(x) if solver.Value(y)]
    path=P/'experiments/checkpoints/cpsat_best.json'
    path.write_text(json.dumps({'blocks':[D[i]['block'] for i in ids], 'candidate_indices':ids},indent=2)+'\n')
    print('Found',len(ids),'blocks in',path)
elif status==cp_model.INFEASIBLE:
    print('INFEASIBLE exact CP-SAT model; reproduce with matching OR-Tools version and seed.')
else:
    print('UNKNOWN is not a proof of infeasibility')
