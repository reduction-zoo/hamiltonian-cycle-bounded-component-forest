# Fixed executable endpoints

Source: `{"vertices": [distinct integer labels], "edges": [[u,v], ...]}`. Vertices are explicitly listed, including isolated vertices. Edges are unordered, distinct, nonloop pairs of listed labels. A Hamiltonian cycle output is a list containing each vertex once, whose consecutive pairs and last-first pair are edges. A simple undirected cycle has at least three vertices, so graphs with fewer than three vertices have output `"NO-SOLUTION"`. The final vertex is not repeated. NO-SOLUTION is valid exactly when no Hamiltonian cycle exists.

Target: `{"weights": [nonnegative integers], "edges": [[i,j], ...], "K": positive integer, "B": positive integer}`. The explicit weights list indexes vertices 0,...,N-1. Edges define a simple undirected graph. Output is `{"blocks": [[vertex indices], ...]}` partitioning all N vertices into at most K nonempty blocks. Each induced block is connected and its weight sum is at most B. The empty graph has the empty partition. NO-SOLUTION is valid exactly when no such partition exists. An optional `"trees"` field may give, for each block, a list of original edges constituting a spanning tree of that block. Recovery must handle valid outputs with or without this optional certificate, in arbitrary block and vertex order.

All integers have arbitrary finite binary encodings; JSON decimal conversion must not impose a fixed digit limit. Numeric capacity, cardinality and weight values are not unary or bounded by a machine word. Source vertex labels have no numerical meaning.

`python3 algorithm.py` reads one source JSON value on stdin and emits F(source). `python3 algorithm.py --extract` reads `{"source": source, "target_solution": output}` and emits G. Diagnostics use stderr; execution errors return nonzero. Both invocations run independently with no retained state. F and G cannot call either source or target oracle.

Source validity is checked by exact vertex and edge tests, with exhaustive enumeration for NO. Target partitions are checked by exact integer sums, coverage and graph traversal; the oracle obtains partitions independently from the actual emitted target. UNKNOWN is an error, not a negative answer.
