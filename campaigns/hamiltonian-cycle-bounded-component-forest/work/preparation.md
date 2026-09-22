# Prepared testing foundation

2026-09-22. Initial commit 7ae0df6. No candidate has been constructed.

The source oracle enumerates vertex permutations with the first listed vertex fixed, tests every cyclic edge, and treats simple undirected cycles as having at least three vertices. Fixing a start retains every cycle up to rotation, including both orientations. Direct validation also accepts other starting vertices.

The target oracle uses Z3 5.1.0 (locked package 5.1.0.0), not a candidate construction. It assigns each vertex a block label and a nonnegative depth below N. Labels introduce nonempty blocks in first-appearance order and range over fewer than min(K,N) labels. Each block's first vertex is its unique depth-zero root. Every other vertex has a same-block neighbor of smaller depth. Strict descent connects every member to the unique root. Conversely, any connected block has a spanning tree rooted at its least-index vertex, whose depths satisfy these constraints. Exact integer sums enforce the capacity bound for each label. Empty graphs have the empty partition. Positive K and B, nonnegative weights and simple-graph legality are checked.

Thus SAT yields exactly the target partitions up to block ordering. After each model the entire label assignment is blocked, not a depth certificate, to obtain alternate partitions. The prepared candidate loop takes up to 12 distinct partitions per instance; reaching this finite output bound is not a proof of exhaustive output coverage. NO-SOLUTION is accepted only after conclusive UNSAT when no partition was found. UNKNOWN raises an execution error. No timeouts.

Independent validators check exact coverage, nonempty blocks, at-most-K count, integer capacity sums and connectivity by graph traversal. Optional tree certificates are checked for original edges, exact block vertices, connectivity and the tree edge count. Source witness validity checks the cycle edges directly; NO uses exhaustive source truth. Neither oracle imports or depends on a candidate.

Command from repository root: `uv sync --locked`; `uv run --no-sync python campaigns/hamiltonian-cycle-bounded-component-forest/work/check.py --self-test`.

Result: 9 source fixtures and 7 target fixtures passed, including alternate partitions, zero weights, empty graphs, impossible capacities, disconnected blocks, and 5,001-digit weights/capacities. Deliberate failures of connectivity, coverage, weight, block count and tree certificates were rejected. Interpreter: uv-selected CPython 3.14.2 at `/opt/local/bin/python3.14`. No execution failure. The locked environment and this foundation must be committed before construction.
