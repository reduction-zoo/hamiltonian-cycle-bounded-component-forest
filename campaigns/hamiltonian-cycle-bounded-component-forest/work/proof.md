# Hamiltonian cycle to two bounded connected blocks

## Endpoints and theorem

The source is an explicit finite simple undirected graph on a listed set of n distinct integer labels. A simple cycle has at least three vertices. Its valid outputs are Hamiltonian cyclic vertex lists, or NO-SOLUTION if none exists. Target weights are nonnegative binary integers; K and B are positive binary integers. Valid outputs partition all vertices into at most K nonempty connected blocks of weight at most B, or NO-SOLUTION exactly when impossible. Optional block spanning trees may accompany the partition. The JSON details and boundary convention are in contract.md.

The algorithms below form a deterministic polynomial-time reduction with recovery from every valid target output. The composition uses positional Boolean clauses, an exact subset sum encoding and two weighted anchors. These intermediate predicates are proved here, not used as algorithmic oracles. No tree is decoded as a path.

## 1. Positional clauses

For n<3, F emits one vertex of weight 2 with K=B=1. It is infeasible, as is the source; G maps its only valid answer NO-SOLUTION to NO-SOLUTION.

For n>=3, fix the first listed source vertex v_0 as the root and put r=n-1. Index the other vertices by v=0,...,r-1 and positions after the root by p=0,...,r-1. There are V=r^2 Boolean variables X_(v,p), numbered i=vr+p. For every position require exactly one vertex, and for every vertex exactly one position: each requirement consists of a positive clause over its r variables and all pairwise negative clauses. For every vertex not adjacent to the root, add unit clauses forbidding it in positions 0 and r-1. For each successive pair p,p+1 of remaining positions and each ordered pair of distinct nonadjacent remaining vertices v,w, add the clause NOT X_(v,p) OR NOT X_(w,p+1).

Every clause is nonempty, contains distinct variables, and has width at most r (since r>=2). A satisfying assignment selects a permutation and requires its consecutive edges and both root edges. Hence it describes a Hamiltonian cycle starting at v_0. Conversely, any Hamiltonian cycle can be rotated to start at v_0 and gives a satisfying assignment. Both orientations are permitted. The number C of clauses and total literal occurrences are O(n^3); V=O(n^2).

## 2. Carry-free subset sum

Let clause j have width w_j. Set h_j=2^ceil(log_2 w_j), with h_j=1 for unit clauses, and choose R=2 max_j h_j. Since n>=3, positive exactly-one clauses have width r>=2, so R>=4. Use digit positions 0,...,V-1 for variables and V,...,V+C-1 for clauses. The integer for a digit vector is its ordinary base-R value.

For each variable i create two positive items, true then false. Each has digit 1 at its variable position. At clause position V+j, its digit is 1 exactly if that truth choice satisfies a literal in clause j, and otherwise 0. For clause j add slack items with sole nonzero digit 1,2,4,...,h_j/2 at V+j; unit clauses have no slack items. The desired sum T has digit 1 at each variable position and h_j at clause position V+j. Number all variable items first in true/false pairs, followed by slack items in clause order and increasing binary weight. Let a_1,...,a_M be the resulting list and S its sum.

No subset of the items produces any carry. At a variable digit the total over all items is two, less than R. At clause digit j it is w_j+h_j-1, since each literal contributes exactly one truth item and the binary slack sums to h_j-1. This is at most 2h_j-1<R. All digits are nonnegative. Thus equality to T is equivalent to equality at every digit.

Any subset summing to T selects exactly one truth item per variable. If t_j is the number of satisfied literals in clause j, its selected slack must sum to h_j-t_j. The available slack realizes exactly the integers 0,...,h_j-1. Because 0<=t_j<=w_j<=h_j, the clause digit can reach h_j if and only if t_j>=1. Therefore every subset summing to T decodes to a satisfying assignment, and every satisfying assignment extends to such a subset by binary slack choices. This argument includes unit clauses without slack. In particular, no carries or negative weights can simulate a satisfied clause.

All a_i and T are positive. Also S>T: the full item sum has digit 2 at each variable position, whereas T has digit 1; at each clause position its digit w_j+h_j-1 is at least h_j. There is no carry, so coordinatewise domination with strict domination at a variable position proves the inequality. These facts justify the positive parameters below.

## 3. Two-anchor connected partition

Create anchor vertices alpha=0 and beta=1 of weights S and 2T. For each item a_i create a vertex of that weight, indexed after the anchors. Join each item to both anchors, with no other edges. This is the simple bipartite graph K_(2,M). Set K=2 and B=S+T. Its total vertex weight is 2S+2T=2B. All weights and parameters are positive.

If a subset I of items sums to T, put alpha and I in one block, and beta and the remaining items in the other. Each block is connected by its anchor edges (a singleton anchor is also connected) and has weight B. Thus a source cycle gives a valid target partition.

Conversely, any valid partition must have exactly two blocks, both of weight B: the positive total weight 2B cannot fit in one block, and neither block can be underfull while the other is at most B. The anchors cannot lie together because their combined weight S+2T exceeds B by T>0. Consequently the block containing alpha contains item weight exactly B-S=T. Its items yield a satisfying assignment and then a Hamiltonian cycle by the preceding two equivalences. This reasoning applies to every legal partition, regardless of block order, vertex order, or supplied spanning trees. Connectivity is satisfied by the image construction but is not incorrectly assumed to imply a path.

## 4. Executable recovery and all outputs

G maps NO-SOLUTION to NO-SOLUTION. For a partition it finds the block containing vertex 0. The true-choice item for variable i has target vertex index 2+2i. For each position p, G finds the unique v whose true-choice item 2+2(vr+p) lies in that block, then returns the root followed by those remaining vertices in position order. It ignores optional tree certificates. It reconstructs clause counts from the source only to check the partition encoding, not to solve a satisfiability or subset-sum instance. Its checks fail explicitly on malformed outputs; validity of the target answer is the mathematical premise.

The preceding equivalences show that the target is feasible exactly when the source has a cycle. Thus NO-SOLUTION is valid for the target exactly when it is valid for the source. Every feasible target output yields a cycle by the anchor block, digit and permutation arguments. Each endpoint has a nonempty valid-output set: finite feasible witnesses or its designated negative answer. The n<3 branch was handled separately. Arbitrary source labels, including large signed integers, enter only through equality and the returned vertex list.

## 5. Worst-case polynomial bounds and overhead

For n>=3, V=O(n^2), C=O(n^3), and the largest clause width is at most n-1. Each h_j<2w_j, so R=O(n). There are D=V+C=O(n^3) digit positions and at most O(log n) slack items per clause. Thus M=O(n^3 log n), and every item and T has O(n^3 log n) bits. S, 2T and B add at most O(log M) bits, so have the same bound. The target has M+2 vertices and 2M edges. Its total encoding length is O(n^6 log^2 n), including weights and explicit edge indices. No integer is expanded into a unary gadget or used as an iteration bound.

Let L be the source encoding length, including its explicit vertex list. Then n<=O(L). Elementary arithmetic on the polynomial-length integers above yields polynomial bit complexity. For a conservative explicit bound, D=O(n^3), M=O(n^4), and all constructed integers have O(n^4) bits. Computing powers by repeated multiplication (or binary powering), updating O(n^3) literal digits, adding O(n^4) slack items, summing the weights and serializing them fits O((L+1)^15) bit operations using school arithmetic and repeated-division integer conversion. This loose bound includes worst-case label hashing/comparison and input validation. Target length is O((L+1)^8). It establishes polynomiality, not an optimized runtime exponent.

For target-output length H, G constructs only the O(n^3) clauses and their widths, scans/sorts the explicit block indices and tests the O(n^2) true-item positions. It performs no arithmetic on the large target weights and no search over assignments. A conservative O((L+H+1)^6) bit bound covers parsing, source validation and these scans. Its cycle output contains exactly the source labels once, hence has O(L+1) bits. Arbitrarily large optional certificates and integer encodings are accounted for in H. Both maps disable the default integer-text digit ceiling.

The weights can be exponentially large in value; the question permits binary integers. This route does not establish a strong-hardness result, a small-numeric-weight construction or efficient target solving. Using two anchors keeps the graph at 2M edges; no complete graph or path-forcing gadget is needed. Further overhead optimization is optional, not an unmet endpoint requirement.

## Attribution and claim limits

The positional clauses are derived and proved directly here. The variable/clause digit method is standard SAT-to-Subset-Sum; the power-of-two slack spelling is proved explicitly for the nonempty clause widths used here. The two-anchor capacity conversion is also proved directly. This is a composed reconstruction from standard ingredients, not a claim of mathematical novelty or a reconstruction of the disputed tree-to-cycle converse. Supporting primary-source checks and exact locations will be recorded in round 001's literature note. The full theorem does not rely on an unaudited external gadget or cited black-box reduction.
