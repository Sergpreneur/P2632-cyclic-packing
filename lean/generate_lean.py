#!/usr/bin/env python3
"""Generate P2632's Lean 4 source from the exact packing and orbit certificates.

This generator NEVER produces a Lean theorem proof from external truth claims:
the Lean files re-evaluate the finite assertions themselves.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
DST=Path(__file__).resolve().parent
blocks=json.loads((ROOT/'certificates/constructions/packing_12.json').read_text())['blocks']
orbtrip=json.loads((ROOT/'data/triples.json').read_text())
from itertools import combinations

def canon(t):
    return min(tuple(sorted((x-a)%31 for x in t)) for a in t)
lookup={tuple(t):i for i,t in enumerate(orbtrip)}
assert len(orbtrip)==145 and len(blocks)==12
assert all(len(b)==5 for b in blocks)
resources=[sorted(lookup[canon(t)] for t in combinations(b,3)) for b in blocks]
assert all(len(x)==10 for x in resources)
assert len(set(sum(resources,[])))==120

blocks_src=',\n'.join('  ['+', '.join(map(str,b))+']' for b in blocks)
base=f'''import Std

/-!
# P2632: twelve-orbit cyclic 3-(31,5,1) packing

Author: Nefedov Sergey
Affiliation: Moscow State University, Mathematics Department

This source directly constructs all 372 translates of the 12 base five-sets,
and independently enumerates their 3720 triple occurrences by *all* index
triples i < j < k in each developed five-set. Each triple is
represented as a *sorted* list of its three residues in [0,30]. Therefore
equality of the normalized triples is equality of unordered 3-subsets.

The expensive finite assertions below use `native_decide`, which depends on
Lean's compiler for evaluation (not kernel-only reduction). There are no
`sorry`, user-added `axiom`, or external oracle in this file. Kernel-only
checks on the 120 orbit resources appear in ResourceCertificate.lean.
-/

namespace P2632

set_option maxHeartbeats 8000000
set_option maxRecDepth 8192

/-- Explicit base blocks as stated in the preprint (zero-based residues). -/
def baseBlocks : List (List Nat) := [
{blocks_src}
]

/-- The ten distinct index choices from a five-element list (5 choose 3). -/
def chooseThree (xs : List Nat) : List (List Nat) :=
  let a := xs.getD 0 0
  let b := xs.getD 1 0
  let c := xs.getD 2 0
  let d := xs.getD 3 0
  let e := xs.getD 4 0
  [ [a, b, c], [a, b, d], [a, b, e], [a, c, d], [a, c, e],
    [a, d, e], [b, c, d], [b, c, e], [b, d, e], [c, d, e] ]

/-- Translation in Z/31Z, followed by normalization of an unordered subset. -/
def shiftAndSort (t : Nat) (xs : List Nat) : List Nat :=
  (xs.map (fun x => (x + t) % 31)).mergeSort

/-- All 31 translates of each of the twelve base blocks (372 entries). -/
def developedBlocks (bs : List (List Nat)) : List (List Nat) :=
  bs.flatMap (fun b =>
    (List.range 31).map (fun t => shiftAndSort t b))

/--
Enumerate all 3-element index choices i < j < k of *any* input block.
Unlike the ten hardcoded templates, this definition exhaustively loops over
all indices of each developed block. For a sorted 5-set, its ten results are
exactly the unordered 3-subsets, without any choice of a triple table.
-/
def enumerateTriples (xs : List Nat) : List (List Nat) :=
  (List.range xs.length).flatMap (fun i =>
    (List.range xs.length).flatMap (fun j =>
      (List.range xs.length).filterMap (fun k =>
        if decide (i < j) && decide (j < k) then
          some [xs.getD i 0, xs.getD j 0, xs.getD k 0]
        else none)))

/-- Every triple in every developed 5-set, enumerated from all index choices. -/
def developedTriples (bs : List (List Nat)) : List (List Nat) :=
  (developedBlocks bs).flatMap enumerateTriples

/-- Check that a numeric list is strictly increasing. -/
def strictlyIncreasing : List Nat → Bool
  | [] => true
  | [_] => true
  | x :: y :: rest => decide (x < y) && strictlyIncreasing (y :: rest)

/-- The list represents a 5-element subset of Z/31Z. -/
def wellFormedFive (xs : List Nat) : Bool :=
  (xs.length == 5) && xs.all (fun x => decide (x < 31)) && strictlyIncreasing xs

/-- The list represents a 3-element subset of Z/31Z. -/
def wellFormedTriple (xs : List Nat) : Bool :=
  (xs.length == 3) && xs.all (fun x => decide (x < 31)) && strictlyIncreasing xs

/-- An explicit, decidable formulation of the cyclic 3-packing predicate. -/
def IsCyclicTriplePacking (bs : List (List Nat)) : Prop :=
  bs.all wellFormedFive = true ∧
  (developedBlocks bs).Nodup ∧
  (developedBlocks bs).all wellFormedFive = true ∧
  (developedBlocks bs).all
    (fun b => decide (enumerateTriples b = chooseThree b)) = true ∧
  (developedTriples bs).Nodup ∧
  (developedTriples bs).all wellFormedTriple = true

/-- Exactly twelve base blocks are supplied. -/
theorem base_count : baseBlocks.length = 12 := by decide

/-- All twelve blocks are genuine five-subsets. -/
theorem base_well_formed : baseBlocks.all wellFormedFive = true := by decide +kernel

/-- The 372 generated developed blocks are genuine five-subsets. -/
theorem developed_five_sets :
    (developedBlocks baseBlocks).all wellFormedFive = true := by
  native_decide

/-- The twelve chosen orbits contain 372 distinct developed blocks. -/
theorem distinct_developed_blocks :
    (developedBlocks baseBlocks).Nodup := by
  native_decide

/-- There are exactly 372 developed blocks. -/
theorem developed_block_count :
    (developedBlocks baseBlocks).length = 372 := by
  native_decide

/-- The independent index-based triple generator agrees with all ten templates. -/
theorem triple_enumeration_complete :
    (developedBlocks baseBlocks).all
      (fun b => decide (enumerateTriples b = chooseThree b)) = true := by
  native_decide

/-- There are exactly 3720 generated triple occurrences. -/
theorem triple_occurrence_count :
    (developedTriples baseBlocks).length = 3720 := by
  native_decide

/-- Every generated triple has three distinct residues in [0,30]. -/
theorem all_triples_well_formed :
    (developedTriples baseBlocks).all wellFormedTriple = true := by
  native_decide

/--
Main formal check: no unordered triple repeats across any of the
12 * 31 developed five-sets. This is the 3-packing constraint itself.
-/
theorem no_repeated_triple :
    (developedTriples baseBlocks).Nodup := by
  native_decide

/-- Single formal result combining the structural and packing checks. -/
theorem twelve_orbit_packing_certificate :
    baseBlocks.length = 12 ∧
    baseBlocks.all wellFormedFive = true ∧
    (developedBlocks baseBlocks).length = 372 ∧
    (developedBlocks baseBlocks).Nodup ∧
    (developedBlocks baseBlocks).all wellFormedFive = true ∧
    (developedTriples baseBlocks).length = 3720 ∧
    (developedBlocks baseBlocks).all
      (fun b => decide (enumerateTriples b = chooseThree b)) = true ∧
    (developedTriples baseBlocks).Nodup ∧
    (developedTriples baseBlocks).all wellFormedTriple = true := by
  exact ⟨base_count, base_well_formed, developed_block_count,
    distinct_developed_blocks, developed_five_sets, triple_occurrence_count,
    triple_enumeration_complete, no_repeated_triple, all_triples_well_formed⟩

/-- Existence of a twelve-orbit cyclic 3-(31,5,1) packing. -/
theorem exists_twelve_orbit_packing :
    ∃ bs : List (List Nat), bs.length = 12 ∧ IsCyclicTriplePacking bs := by
  refine ⟨baseBlocks, base_count, ?_⟩
  exact ⟨base_well_formed, distinct_developed_blocks, developed_five_sets,
    triple_enumeration_complete, no_repeated_triple, all_triples_well_formed⟩

-- `native_decide` generates a native-evaluation axiom in Lean 4.35;
-- these declarations print the exact axioms used on the installed toolchain:
#print axioms no_repeated_triple
#print axioms exists_twelve_orbit_packing

end P2632
'''
(DST/'P2632.lean').write_text(base)

r_src=',\n'.join('  ['+', '.join(map(str,r))+']' for r in resources)
codes=[31*t[1]+t[2] for t in orbtrip]
code_src='\n'.join('  '+', '.join(map(str,codes[i:i+15]))+(',' if i+15<len(codes) else '') for i in range(0,len(codes),15))
resource=f'''import P2632

/-!
# P2632: independent small kernel-reduced triple-orbit certificate

Author: Nefedov Sergey
Affiliation: Moscow State University, Mathematics Department

The following theorem checks, by ordinary *kernel* reduction (`decide +kernel`),
that each of the twelve base blocks uses the stated ten triple-orbit indices,
and that all 120 indices are pairwise distinct. This is the compact certificate
published in the preprint. The direct check in P2632.lean independently checks
all 3720 actual shifted triples, without trusting any precomputed orbit index.
-/

namespace P2632

set_option maxHeartbeats 4000000
set_option maxRecDepth 8192

/-- The 145 canonical triple orbit labels encode (0,a,b) as 31*a+b. -/
def tripleOrbitCodes : List Nat := [
{code_src}
]

/-- Resource-index rows from the mathematical preprint. -/
def publishedResources : List (List Nat) := [
{r_src}
]

/-- Normalize a triple by putting an indicated point at residue zero. -/
def zeroAnchor (a : Nat) (xs : List Nat) : List Nat :=
  (xs.map (fun x => (x + 31 - a) % 31)).mergeSort

/-- Encode an already sorted normalized triple (0,u,v) as 31*u+v. -/
def normalizedCode (xs : List Nat) : Nat :=
  31 * xs.getD 1 0 + xs.getD 2 0

/-- Lexicographically least (0,u,v) among the three cyclic translations. -/
def orbitCode (xs : List Nat) : Nat :=
  let a := xs.getD 0 0
  let b := xs.getD 1 0
  let c := xs.getD 2 0
  min (normalizedCode (zeroAnchor a xs))
    (min (normalizedCode (zeroAnchor b xs))
         (normalizedCode (zeroAnchor c xs)))

/-- Compute each orbit index from the actual base blocks, not the publication. -/
def computedResources : List (List Nat) :=
  baseBlocks.map (fun block =>
    ((chooseThree block).map (fun t => tripleOrbitCodes.idxOf (orbitCode t))).mergeSort)

/-- Verify that the orbit-representative table indeed has 145 distinct entries. -/
theorem triple_orbit_codes_count : tripleOrbitCodes.length = 145 := by decide

theorem triple_orbit_codes_nodup : tripleOrbitCodes.Nodup := by decide +kernel

/-- All twelve certificate rows have ten entries. -/
theorem resource_row_lengths :
    publishedResources.length = 12 ∧
    publishedResources.all (fun row => row.length == 10) = true := by
  decide +kernel

/-- Every resource index is a valid index between 0 and 144. -/
theorem resource_indices_in_range :
    publishedResources.flatten.all (fun n => decide (n < 145)) = true := by
  decide +kernel

/-- No resource index is used more than once among all twelve blocks. -/
theorem all_120_resources_distinct :
    publishedResources.flatten.Nodup := by
  decide +kernel

/-- The actual 12*10 triples reproduce every published resource row. -/
theorem computed_resources_match_published :
    computedResources = publishedResources := by
  decide +kernel

/-- One complete, kernel-reduced proof of the small 120-index table. -/
theorem compact_resource_certificate :
    tripleOrbitCodes.length = 145 ∧
    tripleOrbitCodes.Nodup ∧
    computedResources = publishedResources ∧
    publishedResources.flatten.Nodup ∧
    publishedResources.flatten.all (fun n => decide (n < 145)) = true := by
  exact ⟨triple_orbit_codes_count, triple_orbit_codes_nodup,
    computed_resources_match_published, all_120_resources_distinct,
    resource_indices_in_range⟩

#print axioms compact_resource_certificate

end P2632
'''
(DST/'ResourceCertificate.lean').write_text(resource)
(DST/'lean-toolchain').write_text('leanprover/lean4:v4.35.0\n')
(DST/'lakefile.toml').write_text('name = "p2632"\nversion = "0.2.0"\ndefaultTargets = ["P2632", "ResourceCertificate"]\n\n[[lean_lib]]\nname = "P2632"\n\n[[lean_lib]]\nname = "ResourceCertificate"\n')

print('generated main',len(base),'resource checker',len(resource))
