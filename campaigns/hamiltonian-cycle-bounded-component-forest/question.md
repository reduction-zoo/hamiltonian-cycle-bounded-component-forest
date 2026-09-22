# Hamiltonian Cycle → Bounded-component spanning forest

Fixed board record `website/questions/hamiltonian-cycle-bounded-component-forest.json`, read 2026-09-22. Category: Construction open.

## Source

Given a finite simple undirected graph, return a cycle visiting every vertex exactly once, or NO-SOLUTION. All finite combinatorial structures are explicit and numerical data use binary encoding.

## Target

Given a simple graph, nonnegative integer vertex weights and positive integers K,B, partition its vertices into at most K nonempty connected blocks, each of weight at most B, or return NO-SOLUTION. A spanning tree of each block may also be returned.

## Required result and acceptance

Construct deterministic polynomial-time maps F and G. F must produce a legal target instance, and G(x,y) must return a valid source output for every valid target output y, including NO-SOLUTION. A complete rule may reconstruct a published construction or give a new one; it must specify every gadget, numerical parameter and decoding step.

Deliver executable instance construction and output recovery, a general proof covering all legal inputs and target outputs, and worst-case polynomial time and encoding-size bounds. Cite the actual proof used, or identify a newly derived argument. Check small positive and negative instances with independent solvers; finite tests alone do not establish correctness.

## Context

The task seeks an explicit route from spanning traversal to connected partitioning under component-capacity bounds. Difficulty was not established by a construction attempt in the board record. Connected blocks need not be paths. The construction must enforce a spanning cycle through additional structure rather than decoding an arbitrary tree as a path.

The cited review disputes the attribution and rejects its proposed converse. A valid rule remains to be supplied; this record does not claim that the listed source-specific reduction is already established by the citation. Primary proofs had not been independently re-audited; availability of a complete reconstruction elsewhere remained unassessed. Board literature check: 2026-09-18.

Starting reference: [Problem-Reductions issue 238](https://github.com/CodingThrust/problem-reductions/issues/238). Upstream issue and review discussion checked by the board on 2026-09-18. Its references are reconstruction leads, not independently audited proof sources. No solutions were listed.
