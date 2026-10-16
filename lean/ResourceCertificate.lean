import P2632

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
  33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
  48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 66, 67,
  68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82,
  83, 84, 85, 86, 87, 88, 89, 90, 99, 100, 101, 102, 103, 104, 105,
  106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
  132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146,
  147, 148, 149, 150, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175,
  176, 177, 178, 179, 180, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207,
  208, 209, 210, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 264, 265,
  266, 267, 268, 269, 270, 297, 298, 299, 300, 330
]

/-- Resource-index rows from the mathematical preprint. -/
def publishedResources : List (List Nat) := [
  [0, 23, 24, 26, 27, 28, 50, 52, 53, 54],
  [2, 10, 11, 14, 17, 18, 65, 66, 86, 87],
  [4, 12, 13, 15, 16, 21, 97, 98, 112, 113],
  [5, 8, 22, 64, 71, 72, 121, 123, 126, 134],
  [6, 19, 25, 79, 92, 96, 109, 116, 129, 138],
  [30, 36, 43, 77, 84, 110, 111, 117, 128, 130],
  [33, 37, 39, 42, 44, 51, 89, 91, 120, 122],
  [34, 38, 49, 82, 88, 90, 114, 118, 133, 137],
  [35, 45, 48, 57, 59, 68, 127, 140, 141, 144],
  [55, 58, 61, 69, 70, 73, 103, 136, 139, 142],
  [75, 76, 80, 81, 85, 94, 102, 106, 107, 135],
  [78, 83, 93, 99, 100, 104, 105, 108, 131, 143]
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
