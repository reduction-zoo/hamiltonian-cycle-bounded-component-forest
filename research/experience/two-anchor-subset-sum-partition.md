# Two anchors turn exact subset sum into connected capacity partition

Tags: subset-sum, binary-weights, connected-partition, capacity-saturation, all-output-recovery.

## Claim and applicability

For nonnegative explicit item weights with sum S and target 0<T<=S, add two vertices of weights S and 2T. Join every item vertex to both anchors and add no other edges. With at most two blocks and capacity B=S+T, the total weight is 2B. Every feasible partition has two capacity-tight blocks and separates the anchors. The block containing the S anchor therefore selects items of weight T. Conversely, any such subset gives two connected anchor blocks. Anchor identity, not its numeric weight, determines recovery even when the anchor weights coincide. Optional spanning trees are irrelevant.

The claim requires binary weights to preserve polynomial encoding when originating weights are large. It does not force any block tree to be a path, does not allow negative item weights, and does not handle T=0 through the anchor-separation argument. Values T outside (0,S] need separate treatment.

## Evidence and status

General lemma proved in [proof.md, Section 3](../../campaigns/hamiltonian-cycle-bounded-component-forest/work/proof.md), within [round 001](../../campaigns/hamiltonian-cycle-bounded-component-forest/rounds/001/round.md). The [registered independent review](../../campaigns/hamiltonian-cycle-bounded-component-forest/reviews/initial/review.md) advances the construction, including this lemma. Prepared and additional target checks pass; they are evidence of implementation agreement, not proof. This is an explicitly proved standard-style composition, not a novelty claim. Human expert review remains pending.

## Consequence for search

When the target admits binary capacities, check whether a fully decoded numerical reduction supplies the desired route without a path-forcing gadget. This gives a sparse target graph with 2M edges for M items, but says nothing about efficient target solving or strong hardness.

## Use history

Created and updated with review evidence on 2026-09-22 after deriving the current construction. No later use and no measured discovery benefit. Shared-collection promotion remains pending; the board is read-only.
