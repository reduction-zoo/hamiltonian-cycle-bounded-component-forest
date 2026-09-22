# Bounded-label oracle addendum: advance remains applicable

2026-09-22. I assessed the actual uncommitted `work/check.py` diff from commit `642fcfa750ce11fcca93ac472ce885db50c2013b`, including its surrounding input checks, capacity constraints, output extraction, and model-blocking loop. **Advance remains applicable.** The bounded bit-vector label/depth encoding is equivalent to the previous bounded integer encoding on every legal target input. No repair is required.

## Equivalence and consequences

For n=0 the unchanged early return supplies the empty partition before declaring bit vectors. For n≥1, q=bit_length(n) satisfies n<2^q. Thus n itself, min(K,n), every vertex index v<n, zero, and one are exactly representable; using bit_length(n), rather than bit_length(n−1), correctly covers power-of-two n. This remains true for arbitrarily large encoded K because the actual comparison bound is min(K,n).

Unsigned bit vectors denote nonnegative integers. The new `ULT` and `ULE` bounds therefore admit exactly the old domains 0≤color<min(K,n), color≤v, and 0≤depth<n. All equality comparisons preserve their original meaning. Within the implication guarded by color≠0, subtraction of one cannot underflow, so the earlier-color predecessor test is equivalent to the integer expression. At color zero the implication is true regardless of the wrapped subtraction's value. The root condition is unchanged. Within the admitted nonnegative domain, depth≠0 is equivalent to depth>0, and unsigned depth descent is exactly integer descent.

Consequently, each old legal integer assignment has the same representable bit-vector assignment, and each new assignment decodes to an old one. Strict descent still reaches the unique first vertex of each color; connected blocks still admit a spanning-tree depth certificate below n. Block-label symmetry breaking and gap prevention are unchanged. These facts preserve every target partition up to the same block-order symmetry as before.

Capacity sums retain the exact unsigned encoding approved in `reviews/oracle-refinement/review.md`. Equality of a color and loop index c remains exact because c<min(K,n)≤n. All solver formulas now contain only Boolean and bit-vector operations, so `SolverFor("QF_BV")` matches the actual theory. `as_long()` returns the intended nonnegative label value; the model-blocking constants are also representable. The unchanged UNKNOWN branch raises an execution error rather than returning NO. No conclusion about speed follows from changing the solver route.

## Independent targeted checks

`reviews/bounded-labels/check.py` imports neither the candidate nor either oracle. It constructs the complete bounded structural formula over bit vectors and over their unsigned integer interpretations (`BV2Int`), then asks for an assignment where those formulas disagree. All **51** comparisons returned UNSAT: n∈{1,2,3,4,5,8}, K∈{1,n,n+3}, and empty, path, and complete graphs, with duplicate K values omitted. These cover one-vertex and power-of-two boundaries, multiple colors, and connectivity extremes. The integer interpretation cannot hide a missing old assignment because every integer satisfying the old bounds is representable, as established above.

Command from the repository root:

```
uv run --no-sync python campaigns/hamiltonian-cycle-bounded-component-forest/reviews/bounded-labels/check.py
```

Exit zero. No timeout was introduced. This is a targeted equivalence check, not a rerun of the campaign or candidate suite. The general argument above covers unrestricted n, K, and graphs.

## Retained evidence, execution status, and boundaries

A diff against `d2cb3cd` confirmed that `work/algorithm.py` and `work/proof.md` remain unchanged. I reuse the initial review's construction, all-output recovery, endpoint, bit-complexity, novelty, significance, and completed verification judgments, together with the capacity addendum. No manuscript review is included here.

The parent reports that the intermediate capacity-only rerun was terminated as PID 24440 with exit 143 after partial progress, that the current self-tests passed 9 source and 7 target fixtures, and that the full suite is rerunning as session 48681. These are reported execution statuses, not results independently rerun here. The terminated run is incomplete, never a NO answer. This addendum does not certify the latest full suite as complete; record its actual terminal result separately.

This follow-up uses the same native registered `research-reviewer` context as the initial fresh-context review, not a newly spawned context. No model override was requested. Runtime instructions identify Codex based on GPT-6; the exact backend and per-agent usage are unavailable. The reported default service tier is not independently verified here.

Filesystem access remains unrestricted and collaboration tools remain visible. Directory-only writes and no delegation are instructional constraints, not an observed sandbox, tool denial, or enforced depth cap. I followed them: only `reviews/bounded-labels/` was written, no agents were spawned, and candidate files, tests, prior evidence, previous reviews, sibling repositories, and upstream systems were not changed. The authorized scope remains completion of this campaign followed by stopping.
