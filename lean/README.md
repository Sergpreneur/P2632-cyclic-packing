# Lean 4 formalization of TheoremDB P2632

**Author:** Nefedov Sergey  
**Affiliation:** Moscow State University, Mathematics Department  
**Parameter:** cyclic `3-(31,5,1)` packing  
**Result addressed:** existence of 12 cyclic orbits, i.e. the **lower bound** `M*(31,5,3) >= 12`.

## What is in the proof

`P2632.lean` encodes the twelve published base five-subsets as concrete natural-number lists. It:

1. Builds all 31 modular translates of each of the twelve blocks.
2. Sorts each translated block, representing unordered subsets canonically.
3. Enumerates *every* triple of each developed block using all index combinations `i < j < k` (not a handpicked list).
4. Checks all 372 blocks are distinct and contain five distinct residues from `0..30`.
5. Checks the 3720 resulting triples are valid and pairwise distinct, which is the cyclic 3-packing requirement.
6. States `exists_twelve_orbit_packing`, a theorem giving the explicit twelve-base-block witness.

`ResourceCertificate.lean` provides a second, compact computation matching the published resource-index certificate. It recomputes the 120 triple-orbit indices from the base blocks, checks that they equal the displayed rows, and checks that no index repeats. These small finite checks use `decide +kernel`, which requests kernel reduction rather than Lean's native compiler.

### Trust / verification boundaries

- `native_decide` is used for the large direct 3720-triple calculation. If this module compiles successfully, it gives a Lean theorem, but adds Lean's native compiled evaluation (represented by a generated axiom in Lean 4.35) to the trusted base. **It is not a kernel-only proof.** The source includes `#print axioms` to make the dependency visible.
- The second table checker uses `decide +kernel`; it verifies finite table assertions in the Lean kernel. Together with the direct test, it provides two separate checking routes.
- The local environment in which this package was prepared had **no installed Lean 4 toolchain**, and network access from the execution container was blocked. Consequently **the Lean files have not been compiled or type-checked here**. The author must not describe these files as "Lean-verified" until `lake build` succeeds.
- Python and C++ independent checkers have actually been executed and both passed. Their verified numerical result is 12 base blocks, 372 developed blocks, 3720 distinct triples, and no repeated triple.
- The **upper bound** `M* <= 13` is established in the mathematical preprint by pair-incidence counting; a general abstract Lean proof of the upper bound is **not** included in this artifact. Optimality (`M*=12` vs `M*=13`) remains open in this research package.

## How to run Lean

Install `elan` / Lean from https://lean-lang.org/install/ if not already installed. Lean is pinned to **v4.35.0** in `lean-toolchain`. No Mathlib dependency or mathlib cache download is needed; only Lean's bundled `Std` is used.

```bash
cd P2632/lean
lake build
```

To run modules individually and see the two `#print axioms` statements:

```bash
lake env lean P2632.lean
lake env lean ResourceCertificate.lean
```

The final theorem names are:

```lean
P2632.exists_twelve_orbit_packing
P2632.twelve_orbit_packing_certificate
P2632.no_repeated_triple
P2632.compact_resource_certificate
```

To re-run the external independent cross-check (does NOT substitute for compiling Lean):

```bash
python3 verification/check_model_independently.py
```

To regenerate the Lean literals exactly from the separately stored certificate data:

```bash
python3 generate_lean.py
```

The generator reads `../certificates/constructions/packing_12.json` and `../data/triples.json`. Run the independent checker after any regeneration. The theorem proofs are not imported from Python; they evaluate their own functions at elaboration time in Lean.

## Scope

This establishes (subject to Lean compilation) the **existence of twelve orbits**. It does not provide a global impossibility proof for thirteen orbits, so it does not solve the full P2632 optimization problem.
