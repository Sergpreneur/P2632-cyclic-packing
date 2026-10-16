# Reproducibility and trust record

## Inputs

- Parameter: 31 points, blocks of size 5, triples must occur no more than once.
- Each of the 12 base blocks is developed under all 31 translations modulo 31.
- The canonical 12-block witness is a sorted, newline-separated plaintext file:
  `certificates/constructions/packing_12.txt`.
- SHA-256 of that exact file:
  `bd23ca1859c55628896d6ff76cffe5b0db9291976fc0f7745195d44ce3d78e18`.

## Completed checks (16 October 2026)

The source environment executed the direct Python checker, independent C++17 checker, independent Python check of the Lean literals and triple-orbit table, and the Lean source *structure* check. Counts obtained: 12 base blocks, 372 developed blocks, 3720 distinct triples, 775 uncovered triples; 145 triple orbits and 120 distinct orbit indices used by the witness.

The use of source structure validation is **not** Lean type-checking or proof-checking. A working Lean 4 compiler was absent from this local environment and external download was unavailable.

## Lean 4 trust distinctions

- `P2632.lean` asserts the direct expanded packing condition and discharges large closed propositions using `native_decide`. That method uses native compiled evaluation and a generated axiom, not kernel-only reduction.
- `ResourceCertificate.lean` checks the finite resource table with `decide +kernel`. Its final compact theorem checks the *data* and does not include a formal proof of the general combinatorial bridge theorem.
- The standalone mathematical argument in the paper proves that pairwise disjoint triple-orbit resources ensure no repeated developed triple.
- The repository includes `#print axioms` commands to expose proof dependencies, subject to successful compilation.
- `lake build` is the required compilation and verification step to be run in an environment that has Lean v4.35.0 (e.g. the provided GitHub Actions workflow). A passing native-decide build is not equivalent to a fully kernel-only proof.

## Regenerate Lean literals and figures

From the repository root:

```bash
python3 lean/generate_lean.py
python3 lean/verification/check_model_independently.py
python3 src/enumerate_orbits.py
cd paper && latexmk -pdf -interaction=nonstopmode main.tex
```

`lean/generate_lean.py` regenerates the two Lean modules from the exact JSON witness and triple-orbit list. After regeneration, compare the diff; no regeneration is necessary to verify the release as distributed.

## Upper bound and open target

The pair-incidence argument yields M <= 13. There is neither a 13-orbit solution nor a globally valid impossibility certificate in this release. A target-13 SAT encoding may be exported by `src/packing_sat.py`, but neither a SAT time-out nor a local neighborhood exhaustive search is a proof of target-13 UNSAT.

## Environment

Lean toolchain requested: `leanprover/lean4:v4.35.0`. C++ target: C++17. The witness verifiers are Python-3 standard-library-only. Compilation of the manuscript requires a LaTeX distribution with `amsmath`, `booktabs`, `lmodern`, `needspace` and `hyperref`.
