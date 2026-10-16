import Std

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
  [0, 1, 2, 26, 29],
  [0, 1, 4, 19, 20],
  [0, 1, 6, 14, 15],
  [0, 1, 7, 10, 24],
  [0, 1, 8, 21, 27],
  [0, 2, 6, 12, 19],
  [0, 2, 9, 13, 15],
  [0, 2, 10, 14, 25],
  [0, 2, 11, 21, 24],
  [0, 3, 8, 11, 22],
  [0, 4, 8, 13, 18],
  [0, 4, 11, 16, 26]
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
