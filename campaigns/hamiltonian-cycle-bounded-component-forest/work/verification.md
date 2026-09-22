# Independent target verification

Current candidate: the round-001 construction with radix R=2 max h_j. Original implementation f46ec6b and interrupted original checks are retained; [radix-change.md](../rounds/001/radix-change.md) explains the exact no-carry refinement and execution status. Neither old unfinished run establishes NO or full test completion.

The additional verifier `verify.py` imports neither algorithm.py nor check.py. It executes F and G as separate subprocesses. Source truth enumerates cyclic vertex permutations. Its target oracle handles the K=1 or K=2 domain emitted by this candidate: for K=1 it directly checks the single block; for K=2 it uses Boolean membership with vertex zero fixed to the first block only to remove block-order symmetry. Each block sum is encoded using unsigned bit vectors of width max(1, bit_length(sum(weights))). Every partial sum is nonnegative and at most the total, hence strictly below 2^width: overflow is impossible. Capacity is clamped to min(B,total), an equivalent bound because no subset exceeds total. Z3 QF_BV obtains weight-feasible partitions; direct graph traversal rejects disconnected blocks. Rejected assignments are blocked and search continues, so a negative result requires conclusive exhaustion/UNSAT, not failure of one connectivity check. The fixture domain is finite; up to 12 distinct valid partitions are requested per source. UNKNOWN raises.

Results: [verification-result.txt](../rounds/001/verification-result.txt) records 80 source/actual-target instances: all 76 simple graphs on 0..4 labeled vertices, a five-cycle, a five-vertex articulation graph, and a path/triangle with signed 5,001-digit labels. There were 13 source YES and 67 NO, 97 valid target outputs including NO, and 127 recovery calls. Every feasible partition was also reversed in block and vertex order and supplied with independently constructed spanning trees. All passed. Maximum target size was 122 vertices; maximum weight and capacity lengths were 288 bits. No large-scale solver performance or strong-hardness claim follows.

The prepared general-K label/depth oracle was committed before construction (865be96), self-tested on 9 source and 7 target fixtures, and is independently derived from graph connectivity. Its final exact bounded-bit-vector representation passed all 9 prepared candidate instances and 17 recoveries; see [execution evidence](evidence/oracle-refinement/result.txt) and [representation history](evidence/oracle-refinement/record.md). The candidate and proof are unchanged, so the completed 80-instance verification remains applicable.

Structural figure source `figures/two-anchors.svg` shows anchors and items 1,2,3,M, with exactly their eight incident edges. Remaining items are explicitly omitted by the ellipsis; each has precisely the same two anchor incidences. There is no anchor-anchor or item-item edge. Degree counts are M at either anchor and 2 at every item. Source graph labels and target item ordinals are distinct conventions explained in the caption at writing. This graph specification agrees with forward().

Reproduce from repository root with `uv sync --locked` followed by:

```
uv run --no-sync python campaigns/hamiltonian-cycle-bounded-component-forest/work/check.py --self-test
uv run --no-sync python campaigns/hamiltonian-cycle-bounded-component-forest/work/check.py --candidate campaigns/hamiltonian-cycle-bounded-component-forest/work/algorithm.py
uv run --no-sync python campaigns/hamiltonian-cycle-bounded-component-forest/work/verify.py --candidate campaigns/hamiltonian-cycle-bounded-component-forest/work/algorithm.py
```

No runtime sibling dependencies. Arbitrarily long integer text conversion is enabled. No execution timeout. Finite tests support implementation agreement; proof.md establishes the general theorem and bit complexity.
