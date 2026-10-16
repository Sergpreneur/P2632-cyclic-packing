import json,itertools,random,collections
from pathlib import Path
p=Path(__file__).resolve().parents[1]
cands=json.loads((p/'data/orbit_candidates.json').read_text())
known=json.loads((p/'data/known_9_blocks.json').read_text())['blocks']
ms=[sum(1<<r for r in c['resources']) for c in cands]
lookup={tuple(x['block']):i for i,x in enumerate(cands)}
def canon(a):return min(tuple(sorted((x-y)%31 for x in a)) for y in a)
ids=[lookup[canon(b)] for b in known]
print('known 9 ids:',ids)
print('greedy extensions:',sum(not ms[i]&sum(ms[j] for j in ids) for i in range(len(ms))))
for nd in [1,2,3]:
    ct=0; maxavail=0; cases=0; witness=None
    for missing in itertools.combinations(ids,nd):
        remaining=set(ids)-set(missing)
        used=sum(ms[j] for j in remaining)
        available=[i for i in range(len(ms)) if not ms[i]&used and i not in remaining]
        maxavail=max(len(available),maxavail); cases+=1
        if nd<=2:
            avset=set(available)
            for i in available:
                for j in available:
                    if i<j and not ms[i]&ms[j] and len(remaining)+2>9:
                        witness=(remaining,i,j);break
                if witness:break
        if witness:break
    print(f'drop {nd}: max feasible candidates {maxavail}, found exchange',witness and (len(witness[0]),witness[1:]))
