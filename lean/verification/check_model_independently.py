#!/usr/bin/env python3
"""Independent direct checker for the Lean input (no orbit-table dependence).

Directly enumerates all 31 translations, 5-subsets, and 3-subsets,
then counts collisions. Fails on any discrepancy.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib, json, re, sys

here = Path(__file__).resolve()
ROOT = here.parents[2]
LEAN_DIR = here.parents[1]
BASE = ROOT / 'certificates/constructions/packing_12.json'
blocks = json.loads(BASE.read_text())['blocks']
assert len(blocks)==12
assert all(len(b) == 5 and b==sorted(set(b)) and all(0<=v<31 for v in b) for b in blocks)

# Validate each of the ten triple templates actually used by the Lean function.
TEMPLATES = [(0,1,2), (0,1,3), (0,1,4), (0,2,3), (0,2,4),
             (0,3,4), (1,2,3), (1,2,4), (1,3,4), (2,3,4)]
assert TEMPLATES == list(combinations(range(5),3))

# Ensure the source's literal blocks have not drifted from JSON.
src = (LEAN_DIR/'P2632.lean').read_text()
blocks_chunk = src.split('def baseBlocks : List (List Nat) := [',1)[1].split('\n]',1)[0]
source_rows = [[int(x) for x in re.findall(r'\d+', row)] for row in blocks_chunk.splitlines() if row.strip().startswith('[')]
assert source_rows == blocks, 'Lean base blocks do not match the certified JSON input'

expanded_blocks = []
triples=[]
for base in blocks:
    for shift in range(31):
        shifted=tuple(sorted((x+shift)%31 for x in base))
        expanded_blocks.append(shifted)
        triples.extend(combinations(shifted,3))
assert len(expanded_blocks)==372 and len(set(expanded_blocks))==372
assert len(triples)==3720 and len(set(triples))==3720
assert all(len(set(t))==3 for t in triples)
assert all(len(b)==5 and len(set(b))==5 for b in expanded_blocks)

# Independent orbit rows without reliance on published numbers.
all_triple_orbits=sorted({min(tuple(sorted((x-a)%31 for x in t)) for a in t)
                          for t in combinations(range(31),3)})
assert len(all_triple_orbits)==145
lookup={t:i for i,t in enumerate(all_triple_orbits)}
rows=[]
for b in blocks:
    rows.append(sorted(lookup[min(tuple(sorted((x-a)%31 for x in t)) for a in t)]
                       for t in combinations(b,3)))
assert len(set(sum(rows,[])))==120
resource_src=(LEAN_DIR/'ResourceCertificate.lean').read_text()
res_chunk=resource_src.split('def publishedResources : List (List Nat) := [',1)[1].split('\n]',1)[0]
source_resources=[[int(x) for x in re.findall(r'\d+', row)] for row in res_chunk.splitlines() if row.strip().startswith('[')]
assert source_resources==rows
codes_src=resource_src.split('def tripleOrbitCodes : List Nat := [',1)[1].split('\n]',1)[0]
source_codes=[int(x) for x in re.findall(r'\d+', codes_src)]
assert source_codes==[31*t[1]+t[2] for t in all_triple_orbits]

result={
  'status':'PASS: independent Python model (NOT a Lean compiler result)',
  'base_blocks':12,
  'developed_blocks':372,
  'unique_developed_blocks':len(set(expanded_blocks)),
  'triple_occurrences':3720,
  'unique_triples':len(set(triples)),
  'duplicate_triples':len(triples)-len(set(triples)),
  'total_available_triples':len(list(combinations(range(31),3))),
  'triple_orbit_count':145,
  'used_orbit_resources':len(set(sum(rows,[]))),
  'lean_input_sha256':hashlib.sha256((LEAN_DIR/'P2632.lean').read_bytes()).hexdigest(),
  'lean_resources_sha256':hashlib.sha256((LEAN_DIR/'ResourceCertificate.lean').read_bytes()).hexdigest(),
}
out=LEAN_DIR/'verification'/'independent_check.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
