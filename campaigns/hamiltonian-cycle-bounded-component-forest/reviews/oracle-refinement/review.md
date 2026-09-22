# Oracle refinement addendum: advance remains applicable

2026-09-22. This focused follow-up assesses the current uncommitted capacity-encoding change in `work/check.py` against HEAD `d2cb3cdc4f8d8e0638a6ebcdbc75364d59013b1e`. The initial advance in `reviews/initial/review.md` remains applicable. No repair is required for this change.

## Scope and retained evidence

I read the current `AGENTS.md`, `work/evidence/oracle-refinement/record.md`, the actual checker diff, and the surrounding `target_solutions` implementation. A diff against the initial-review commit showed no changes to `work/algorithm.py` or `work/proof.md`. I reuse the initial construction, recovery, novelty, significance, and completed 80-instance verification assessments. I did not rerun either full suite or review the manuscript. The latest scope is only this campaign, followed by stopping; no next campaign is authorized.

The actual change replaces each integer capacity sum with an unsigned bit-vector sum. Integer block labels, depth constraints, connectivity semantics, symmetry breaking, output blocking, model extraction, direct partition validation, and UNKNOWN handling remain unchanged in the inspected diff. The empty-target return still precedes the arithmetic.

## General arithmetic argument

The existing legality check requires every weight to be a nonnegative integer and B to be positive. Write S for the sum of all weights and q=max(1,bit_length(S)). Then 0≤S<2^q, including S=0. Every individual weight, every selected partial sum, and every final color sum lies between zero and S. Each literal weight is therefore representable without truncation, and every bit-vector addition agrees with integer addition without overflow, for every assignment of labels and any admitted K.

The comparison constant min(B,S) is also exactly representable. Since a color sum W always satisfies W≤S, the propositions W≤B and W≤min(B,S) are equivalent. `z3.ULE` implements the required unsigned order, including values whose top bit is set. Unused colors have sum zero and satisfy the bound, as in the original integer encoding. The all-zero-weight case uses one-bit zero sums and bound zero; it imposes no spurious restriction. These facts prove equivalence of the old and new capacity constraints under the existing input premises. Mixing integer label/depth expressions with bit-vector sums through Boolean `If` conditions does not alter that equivalence.

The width depends on encoded weight length, not numeric value, so the representation remains polynomial in the explicit input size. This says nothing about Z3 solving speed. A solver failure or UNKNOWN still raises an error and cannot certify infeasibility.

## Independent targeted check

`reviews/oracle-refinement/check.py` imports neither candidate nor either oracle. It enumerates three-color assignments for six small weight lists and compares evaluated bit-vector sums and unsigned bounds with Python's exact integers. Cases cover zero totals, empty color classes, the signed/unsigned boundary, power-of-two totals, 258-bit weights, and bounds larger than the chosen bit width. From the repository root:

```
uv run --no-sync python campaigns/hamiltonian-cycle-bounded-component-forest/reviews/oracle-refinement/check.py
```

Exit zero: **2,106 exact-sum and capacity comparisons passed**. These finite checks exercise the actual arithmetic operators; the preceding argument establishes the unrestricted equivalence. No execution timeout was introduced.

## Execution status and isolation

The retained record says the previous CLI was interrupted to change service tier; session 51214 was missing on resume and the previously observed process was absent. Its last retained result was partial. That is incomplete execution, not NO or a completed suite. The parent reports that the refined checker self-tests passed and the complete candidate suite is rerunning. I do not certify that suite as complete or infer a speedup from this encoding change. The unaffected completed verification remains valid.

This is a follow-up in the same native registered `research-reviewer` context as the initial fresh-context review; it is not a newly spawned independent context. No model override was requested. Runtime instructions identify Codex based on GPT-6; the exact backend and measured per-agent usage are unexposed. The reported default service tier is a user/process report, not an independently verified billing or model fact.

Filesystem permissions remain unrestricted, and collaboration tools are visible. Directory-only writes and no delegation are enforced by instructions, not a filesystem sandbox, tool denial, or observed depth cap. I followed those boundaries: writes are confined to `reviews/oracle-refinement/`, with no candidate, original test, earlier evidence, initial-review, sibling-repository, or upstream changes. No agents were spawned. The initial advance remains valid with its existing novelty and performance limits; record the prepared suite's final outcome separately when it actually terminates.
