# Round 001 — positional clauses, carry-free subset sum, two anchors

## Plan

Gap: connected blocks may branch, so an arbitrary block tree cannot recover a Hamiltonian cycle. Attempt a complete composed construction using numerical capacity to encode an ordering, without decoding trees as paths.

Mechanism: fix the first source vertex as cycle root, encode a permutation of the remaining vertices by positional Boolean variables and cyclic adjacency clauses. Encode these clauses in a carry-free subset-sum instance with one digit per variable and clause, binary slack for clause satisfaction. Turn subset sum into a two-bin partition with two numerical anchor weights, and connect every item to both anchors. Capacity saturation must separate anchors and reveal a subset from the block containing the designated anchor. Each intermediate equivalence and every-output decoder will be proved; no endpoint is changed and neither map may call a solver.

First discriminating check: prepared triangle YES, path NO, and articulation NO, solved as actual connected-partition targets. Failure may indicate clause boundary errors, carry leakage, anchor ambiguity or oracle scaling; distinguish these causes explicitly. Quantify bit growth before expanding tests. Finite verification scope if the first suite passes: all simple graphs on at most four labeled vertices and selected five-vertex cases, plus alternate target partitions, optional trees and label encodings. No wall-clock limits.

Prior evidence: Prepare commit 865be96 passes exact cycle and partition fixtures. Shared-experience search for Hamiltonian, capacity, partition, subset-sum and satisfiability on 2026-09-22 found no applicable entries. This is one declared composed mechanism. Supporting primary literature checks address attribution of its standard ingredients, not a separate novelty search round.

## Evidence and diagnosis

The candidate and [general proof](../../work/proof.md) are complete. They use two anchor vertices with only 2M edges and binary-encoded weights, not a dense complete graph or a tree-to-path assumption. [Supporting literature](literature.md) attributes the standard digit mechanism and records the starting issue's limitation.

The two independent target formulations now both have completed evidence. The prepared general-K label/depth formulation passed 9 candidate instances and 17 recoveries, after its bounded variables and capacity arithmetic were expressed exactly as unsigned bit vectors. The additional Boolean two-block formulation with direct connectivity filtering passed 80 instances, 97 valid target outputs and 127 recoveries. Self-tests cover 9 source and 7 target fixtures. See [verification](../../work/verification.md) and [oracle rerun](../../work/evidence/oracle-refinement/result.txt).

Outcome: supported. The [registered independent review](../../reviews/initial/review.md) advances the complete construction and independently enumerates 131,072 assignments for each of triangle and path. Its [capacity addendum](../../reviews/oracle-refinement/review.md) proves exact arithmetic equivalence and checks 2,106 assignments. The final bounded-label representation has a focused follow-up review. No substantive proof repair or new mechanism was needed. The radix parameter and oracle representation changes remain in this round.

Four incomplete executions are retained: two original-radix runs canceled before its refinement, the prepared run lost during the user-requested CLI interruption, and the capacity-only mixed-theory run superseded by bounded labels. [Partial progress](progress.txt), [radix change](radix-change.md) and [oracle record](../../work/evidence/oracle-refinement/record.md) distinguish them from completed results. None certifies NO; no solver timeout was introduced.

Experience extraction: [two-anchor subset sum](../../../../research/experience/two-anchor-subset-sum-partition.md), one distinct entry created and updated with review, one pending shared promotion. No measured discovery benefit or token saving is claimed. The English five-page paper was compiled and visually inspected; the [inspection record](../../work/evidence/paper/inspection.md) records repairs and final checks.

## Next action

Commit the completed evidence and manuscript, then stop as instructed. Human expert review is pending, not a reason to start another campaign. Budget: 20 authorized, 1 used, 19 unused; 1 distinct composite mechanism. No claim of strong hardness, earliest priority or practical target-solving performance.
