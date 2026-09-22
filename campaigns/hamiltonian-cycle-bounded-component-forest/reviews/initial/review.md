# Independent review: advance

Reviewed on 2026-09-22 against commit `2a43820cd423211fc2586aef5a4a15e6e2e9171b` and the actual working files. **Advance** under the fixed question's explicit allowance for a reconstructed reduction. The construction, executable recovery, and general bit-complexity argument meet that question. This decision supports expert review; it does not establish mathematical novelty or publication acceptance. No correctness repair is required.

## Scope and isolation

I read `AGENTS.md`, `README.md`, `.codex/agents/research-reviewer.toml`, `.agents/skills/research-review/SKILL.md`, `research/reduction.md`, and `harness/README.md`; the fixed `question.md`; `work/algorithm.py`, `proof.md`, `contract.md`, `preparation.md`, `verification.md`, `check.py`, `verify.py`, and `figures/two-anchors.svg`; and round-001 literature, execution, and verification records. Paths below are relative to this campaign unless stated otherwise.

The route was the native registered `research-reviewer`, requested with `fork_turns=none` and no model override. I received a fresh task context rather than the proposer's reasoning transcript. Runtime instructions identify Codex based on GPT-6; an exact backend identifier and per-agent measured usage are not exposed here. I cannot certify a distinct model from the proposer and claim no token savings.

Filesystem access was unrestricted (`danger-full-access`, approval policy `never`), and collaboration/spawn tools were visible. No filesystem sandbox, tool denial, or enforced delegation-depth cap protected the review boundary. Directory-only writes and no delegation were instructional constraints, which I followed. All reviewer writes are in `reviews/initial/`; no agent was spawned, candidate or original test changed, earlier evidence overwritten, or publication/upstream action taken. The initial repository status was clean. The parent reported that the candidate would remain unchanged during review; I assessed the files themselves, not the reported confidence or test count.

## Correctness

The endpoint in `work/contract.md` matches `question.md`: search for a simple undirected Hamiltonian cycle, including a negative answer, maps to connected vertex partitions with nonnegative binary weights, positive K and B, and at most K blocks. Optional spanning-tree certificates are supported by ignoring them during recovery. The convention that a simple cycle needs three vertices is explicit. Every legal endpoint instance has either a witness or its designated negative answer.

`work/algorithm.py:25–44` implements the positional clauses in `work/proof.md`, Section 1. Row and column exactly-one constraints give a permutation of all nonroot vertices. Root nonadjacency prohibits the first and last positions, and the successive-position clauses prohibit every remaining nonedge. Distinct-position and distinct-vertex constraints justify excluding v=w from that last loop. This gives both directions for Hamiltonian cycles, including either orientation and arbitrary input vertex order.

`work/algorithm.py:53–64` agrees with the carry argument in Section 2. For width w, the implemented ceiling is the smallest power of two at least w. Binary slack sums to h−1, and the full clause digit is w+h−1 < 2h ≤ R. Variable digits total two, strictly below R because the admitted nontrivial branch contains width-r clauses with r≥2. Thus even choosing both truth items cannot introduce a carry. Matching a variable digit forces exactly one truth choice; matching a clause digit is possible precisely when at least one literal is true. Unit clauses correctly have no slack. All items are positive, and full-sum digitwise domination gives S>T>0.

`work/algorithm.py:65–68` and Section 3 use these last inequalities correctly. Total weight is 2B; at most two blocks therefore means exactly two blocks, each of weight B. The anchor pair weighs S+2T>B, so the anchors separate in every valid output. The block containing vertex zero selects item sum T. Conversely, a subset of sum T gives two connected stars. No degree restriction, tree-to-path converse, special target solver behavior, or preferred partition is assumed. The SVG source specifies precisely the eight edges incident to its four displayed item representatives; its ellipsis is consistent with this graph family. I inspected its source, not a rendered manuscript figure.

`work/algorithm.py:71–100` uses the correct true-item indices and recovers the positional permutation from the block containing vertex zero. Coverage and shape checks do not exclude any legal image partition. Block order, vertex order, and optional trees do not affect recovery. G need not independently validate capacities or solve target feasibility: the contract supplies a valid target output. The negative branch is justified by both feasibility implications, rather than merely forwarding an unproved answer. For n<3, the explicit overweight singleton is a legal infeasible target.

Section 5's bounds are conservative but sufficient. There are O(n³) clauses and literal occurrences, O(n³ log n) items, O(n³ log n) bits per integer, and O(n⁶ log² n) output bits. The code's repeated exponentiation and arbitrary-precision arithmetic operate on polynomial-length integers, never iterating to a weight's value. Label comparisons/hashing and decimal conversion remain polynomial in full input length even under collisions; their cost is not assumed constant. G's list membership and sorting fit the stated loose polynomial bound in source plus output length. The integer-text digit limit is disabled in both CLI modes. No algorithmic oracle call appears in F or G.

## Executable evidence and limitations

I inspected the actual two target formulations. In `work/verify.py`, width `bit_length(sum(weights))` prevents unsigned overflow for every subset and partial sum; exact capacity tests plus independent connectivity traversal characterize the K≤2 targets it receives. Rejected disconnected assignments are blocked, not mistaken for infeasibility. In `work/check.py`, strictly descending same-color depths reach the unique first vertex of each color; every connected block admits those depths. Symmetry breaking preserves partitions up to block order. Neither solver imports candidate logic.

`rounds/001/verification-result.txt` records the completed independent actual-target run: 80 instances, 97 outputs, and 127 recovery calls, including negative answers, alternate partitions, reversed ordering, optional trees, and signed 5,001-digit labels. This is recorded earlier evidence, not a suite I reran. The 12-partition limit is not exhaustive all-output coverage; the general proof supplies that coverage.

My added `reviews/initial/check.py` imports neither candidate nor main oracles. It invokes F and G through their CLIs, enumerates every two-block assignment with vertex zero fixed to remove only block-order symmetry, checks actual weights and graph connectivity, and validates recovered cycles directly. Running `uv run --no-sync python campaigns/hamiltonian-cycle-bounded-component-forest/reviews/initial/check.py` from the repository root exited zero:

```
path: 131072 assignments exhausted, 0 valid partitions; recovery passed
triangle: 131072 assignments exhausted, 2 valid partitions; recovery passed
```

The separate prepared general-K candidate runner is still solving its larger cases according to the current verification record; it has **not** passed as a completed suite. Its preparation self-tests and the completed alternative verifier are distinct evidence. The canceled original-radix executions in `rounds/001/radix-change.md` remain incomplete executions, never negative answers. I introduced no timeout. The current R=2 max h refinement preserves the strict no-carry inequalities; no runtime improvement is inferred from the cancellation history.

## Novelty and attribution

Independent web checks on 2026-09-22 covered the final composition, including searches for connected partition/subset-sum and bounded-component spanning-forest hardness. The relevant inspected primary sources were:

- Schoefield and Tardos, [*Subset Sum is NP-complete*](https://www.cs.cornell.edu/courses/cs4820/2018fa/lectures/subset_sum.pdf), Theorem 1 and Claims 2–3, pp. 1–3. These give paired truth items, variable/clause digits, no-carry reasoning, and clause slack. The local binary-slack refinement is explicitly proved rather than attributed verbatim to these notes.
- Heule, [*Chinese Remainder Encoding for Hamiltonian Cycles*](https://www.cs.cmu.edu/~mheule/publications/HamiltonianCycle.pdf), Introduction, pp. 1–2, and Section 3. These establish existing Hamiltonian SAT encoding context; the candidate does not use or claim to reconstruct Heule's particular encoding.
- [Issue 238](https://github.com/CodingThrust/problem-reductions/issues/238), Construction and Correctness. Its proposed converse assumes that a spanning tree's endpoint path visits all vertices. The current candidate makes no such assumption. The issue's arbitrary chosen edge also need not belong to a Hamiltonian cycle, so its displayed forward path construction is not an independently usable proof.

Search surfaced the Garey–Johnson ND10 entry and other connected-partition formulations, but a primary-book PDF fetch failed. I therefore do not certify the book's attribution or original proof. I have not established earliest priority for the two-anchor lemma or ruled out an identical published full composition. Neither gap is evidence of novelty. The candidate's own claim—an explicit composition of standard ingredients, with no mathematical novelty claim—is supported. The fixed question explicitly accepts reconstruction, so existing hardness and standard ingredients do not trigger a novelty-based stop here.

## Significance and remaining work

The concrete contribution is a fully specified F/G rule for the exact requested endpoints, with every-output recovery and a sparse K_(2,M) target. It repairs the substantive absence of a valid converse in the starting proposal. Its significance is constructive and reproducible, not a new complexity classification or efficient Hamiltonian solver. The loose encoding bound and exponentially large numerical values are disclosed; the small completed test domain and unfinished general-K run provide no scalability guarantee. No fixed requirement calls for unary weights, strong hardness, or a faster target solver.

The shared experience directory was read in place and contained only its README, so no prior shared result supports the proof. The new local `research/experience/two-anchor-subset-sum-partition.md` has the correct premises 0<T≤S and nonnegative item weights; these hold here with S>T. Its T=0 caveat and anchor-identity decoding are accurate.

Advance to the authorized writing and expert-review stage. Preserve the incomplete-run status until the prepared runner actually terminates, and keep priority and practical-performance claims within the stated limits. No candidate repair or additional full-suite rerun is a prerequisite of this review decision.
