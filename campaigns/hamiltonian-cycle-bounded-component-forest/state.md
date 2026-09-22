# Campaign state

Status: **ready_for_expert_review**. Budget: 20 research rounds, 1 completed, 19 unused, 1 distinct composite mechanism. Initial commit 7ae0df6; Prepare 865be96 committed before construction; reviewed candidate and additional verification 3a29d27; initial review d2cb3cd; capacity refinement 642fcfa. The executable maps, [general proof](work/proof.md), passing checks, independent advance and [compiled five-page paper](work/manuscript.pdf) agree. This is an agent assessment, not human certification or a novelty claim.

Fixed endpoints are unchanged. Positional Hamiltonian-cycle clauses feed carry-free subset sum and a two-anchor capacity-saturating connected partition. The proof covers every valid target output, NO-SOLUTION, small graphs, arbitrary integer encodings, and polynomial bit complexity. Neither map invokes a solver. The construction composes standard ingredients; no new complexity classification, strong-hardness or practical solver-performance claim is made.

Checks: [Prepare](work/preparation.md) self-tests passed 9 source and 7 target fixtures. Its final general-K oracle passed all 9 candidate instances/17 recoveries ([terminal evidence](work/evidence/oracle-refinement/result.txt), exit zero). [Additional verification](work/verification.md) passed 80 actual target instances, 97 valid outputs and 127 recovery calls, including alternate block/vertex order and optional spanning trees. The finite instance/output bounds do not establish the unrestricted theorem. No solver or subprocess timeout was used.

Independent assessment: [initial registered fresh-context review](reviews/initial/review.md) advances correctness and the reconstruction contribution, with exhaustive 131,072-assignment checks for each of triangle and path. [Capacity addendum](reviews/oracle-refinement/review.md) preserves advance with 2,106 independent arithmetic checks; [bounded-label addendum](reviews/bounded-labels/review.md) preserves advance with 51 structural-equivalence checks. The parent independently reran both addendum scripts successfully. Follow-ups reused the initial reviewer context and unaffected evidence; they were not represented as newly isolated reviews. Candidate and proof stayed unchanged during all reviews.

The English Typst paper was compiled successfully and visually inspected; [inspection](work/evidence/paper/inspection.md) records the five-page pass and final affected-page reinspection. Its figure and equations agree with the construction. Human expert review and optional, unrequested Lean formalization remain pending. Neither blocks this authorized closeout.

## Capability probe — 2026-09-22

- Python 3.14.7 at `/opt/homebrew/bin/python3`; uv 0.12.7 at `/Users/xiweipan/.local/bin/uv`: available. Campaign uv interpreter is CPython 3.14.2 at `/opt/local/bin/python3.14`; Z3 5.1.0 (locked package 5.1.0.0) is available and self-tested.
- Typst 0.15.1 and pdftoppm 26.09.0 at `/opt/homebrew/bin`: available.
- Lean 4.34.0 and Lake 5.0.0-src+293d5d0 at `/Users/xiweipan/.elan/bin`: available. Mathlib not established; formalization optional and unrequested.
- External technical-writing skill at `/Users/xiweipan/.codex/plugins/cache/sci-brain/sci-brain/0.5.0/skills/how-to-technical-writing/SKILL.md`: available and read in this session; reapply for manuscript.
- Codex registered research-reviewer used via native agent_type research-reviewer, fork_turns none, inherited route with no model override. Exact backend and per-agent usage are not exposed; the reviewer reports runtime instructions identifying Codex based on GPT-6. Tool metadata advertises gpt-6-astra, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna and gpt-5.5 overrides; none selected or tested here. The initial context was fresh, but filesystem access was unrestricted and collaboration tools visible. Reviewer-only writes and no delegation were instructional boundaries, not sandbox or depth-limit enforcement. See the reviews' isolation records.
- User-reported resumed setting: Fast OFF, service_tier="default". No independent billing verification or claim of backend change. A goal-tool snapshot on 2026-09-22 measured 832,563 cumulative session tokens and 4,886 seconds across the earlier multi-campaign goal, not this campaign alone. Per-campaign usage and token savings are unavailable; none are estimated.

## Round table

| Round | Mechanism or standalone literature scope | First discriminating check | Outcome | Record |
|---|---|---|---|---|
| 001 | Positional clauses → carry-free subset sum → two anchors | Prepared triangle, path and articulation targets | Supported; independently advanced | [Round](rounds/001/round.md) |

Experience: 1 distinct entry created and updated with reviewed evidence, 1 pending shared promotion: [two-anchor subset sum](../../research/experience/two-anchor-subset-sum-partition.md). No shared collection was modified and no discovery benefit is claimed. Final extraction found no additional supported reusable claim needing a separate entry.

Execution history: four incomplete runs are preserved. Two original-radix runs were canceled with exit 143 ([radix-change.md](rounds/001/radix-change.md)); the user-requested CLI SIGINT left the prepared run unavailable, with no terminal result; the capacity-only mixed-theory rerun was explicitly superseded and exited 143 ([record](work/evidence/oracle-refinement/record.md)). These are execution failures/incomplete runs, never NO certificates. The final rerun completed; no campaign-owned execution remains pending.

Stop decision: completed result and explicit latest user boundary. Finish ONLY this campaign, then STOP. Earlier queue continuation and its stored goal text are superseded; no next question is initialized or researched. Preserve completed sibling results. No publication, remote creation, upstream message, merge or board edit occurred. Next action outside this session is human expert review if desired; there is no remaining authorized campaign work.
