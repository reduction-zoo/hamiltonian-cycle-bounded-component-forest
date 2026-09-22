# Round 001 — positional clauses, carry-free subset sum, two anchors

## Plan

Gap: connected blocks may branch, so an arbitrary block tree cannot recover a Hamiltonian cycle. Attempt a complete composed construction using numerical capacity to encode an ordering, without decoding trees as paths.

Mechanism: fix the first source vertex as cycle root, encode a permutation of the remaining vertices by positional Boolean variables and cyclic adjacency clauses. Encode these clauses in a carry-free subset-sum instance with one digit per variable and clause, binary slack for clause satisfaction. Turn subset sum into a two-bin partition with two numerical anchor weights, and connect every item to both anchors. Capacity saturation must separate anchors and reveal a subset from the block containing the designated anchor. Each intermediate equivalence and every-output decoder will be proved; no endpoint is changed and neither map may call a solver.

First discriminating check: prepared triangle YES, path NO, and articulation NO, solved as actual connected-partition targets. Failure may indicate clause boundary errors, carry leakage, anchor ambiguity or oracle scaling; distinguish these causes explicitly. Quantify bit growth before expanding tests. Finite verification scope if the first suite passes: all simple graphs on at most four labeled vertices and selected five-vertex cases, plus alternate target partitions, optional trees and label encodings. No wall-clock limits.

Prior evidence: Prepare commit 865be96 passes exact cycle and partition fixtures. Shared-experience search for Hamiltonian, capacity, partition, subset-sum and satisfiability on 2026-09-22 found no applicable entries. This is one declared composed mechanism. Supporting primary literature checks address attribution of its standard ingredients, not a separate novelty search round.

## Evidence and diagnosis

The candidate and [general proof](../../work/proof.md) are complete. They use two anchor vertices with only 2M edges and binary-encoded weights, not a dense complete graph or a tree-to-path assumption. [Supporting literature](literature.md) attributes the standard digit mechanism and records the starting issue's limitation.

Two independent target formulations are running: general integer labels/depth connectivity in check.py and exact unsigned bit-vector sums with direct connectivity filtering in verify.py. The latter uses enough bits for the sum of all nonnegative weights, so no subset sum can overflow. [Partial progress](progress.txt) is retained without interpreting unfinished cases as NO. Final verification, independent review and experience extraction remain pending.

## Next action

Implement the finite construction, prove each direction, run the prepared target oracle before further verification.
