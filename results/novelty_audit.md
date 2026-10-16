# Novely audit: verified vs. conjectural

**Mathematically verified new-to-the-record result:** A 12-orbit cyclic 3-(31,5,1) packing exists. TheoremDB P2632 still displays 9 <= M <= 13 (2026-10-16). Therefore the previously recorded lower bound improves **from 9 to 12**.

**Proof strength:** strong for the constructive existence claim. The twelve 5-sets are explicit. Independent Python and C++ direct-shift verifiers exhaustively check 372 translated blocks and 3720 distinct triples; the 120 disjoint triple-orbit resources supply a second finite certificate.

**Full solution?** No. There is still the open dichotomy M*=12 vs M*=13. No global SAT UNSAT proof, no complete branch-and-bound exclusion, and no mathematical upper bound below 13.

**Additional local exact fact:** fixing four or more base blocks from the exhibited 12-orbit packing precludes a 13-orbit completion. An exhaustive 495-neighborhood backtracking program checked all possibilities containing four of the exhibited blocks (see exact_local_d8.log); this is not a global prohibition of 13.

**Publication assessment:** suitable as a short *construction note / computational result*, conditional on a stronger novelty audit, author verification, and publication-policy disclosures. To target a substantial combinatorics journal, resolving M*=12 or13, developing a general family, or producing a deeper theorem would materially strengthen the work.

**Authorship:** The preprint is attributed to Nefedov Sergey (Moscow State University, Mathematics Department), as specified by the author. Independent human scrutiny of the mathematics and applicable journal disclosure requirements for AI assistance remain important before external submission.
