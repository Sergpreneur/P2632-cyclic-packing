import json, itertools
from pathlib import Path
p=Path(__file__).resolve().parents[1]
cands=json.loads((p/'data/orbit_candidates.json').read_text())
known=json.loads((p/'data/known_9_blocks.json').read_text())['blocks']
ms=[sum(1<<r for r in c['resources']) for c in cands]
lookup={tuple(x['block']):i for i,x in enumerate(cands)}
def canon(a):return min(tuple(sorted((x-y)%31 for x in a)) for y in a)
ids=[lookup[canon(b)] for b in known]
for missing in ids:
    remaining=set(ids)-{missing}
    used=sum(ms[j] for j in remaining)
    available=[i for i in range(len(ms)) if not ms[i]&used and i not in remaining]
    for i in available:
        for j in available:
            if i<j and not ms[i]&ms[j]:
                found=sorted(remaining|{i,j})
                path=p/'data/best_packing.json'
                path.write_text(json.dumps({'blocks':[cands[k]['block'] for k in found], 'candidate_indices':found,'method':'one-to-two exchange from TheoremDB 9'},indent=2)+'\n')
                print('removed',missing,cands[missing]['block'],'inserted',i,j)
                print('10 blocks:')
                for k in found: print(cands[k]['block'])
                quit()
print('NO')
