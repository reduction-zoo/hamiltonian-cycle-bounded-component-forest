"""Independent symbolic equivalence check for bounded connectivity labels/depths."""
import z3

checks = 0
for n in (1, 2, 3, 4, 5, 8):
    for k in sorted({1, n, n+3}):
        for shape in ("empty", "path", "complete"):
            edges = {(u, v) for u in range(n) for v in range(u+1, n)
                     if shape == "complete" or (shape == "path" and v == u+1)}
            colors = [z3.BitVec(f"c{i}", n.bit_length()) for i in range(n)]
            depths = [z3.BitVec(f"d{i}", n.bit_length()) for i in range(n)]
            integer_colors = [z3.BV2Int(c) for c in colors]
            integer_depths = [z3.BV2Int(d) for d in depths]
            formulas = []
            for cs, ds, less, leq in (
                (colors, depths, z3.ULT, z3.ULE),
                (integer_colors, integer_depths, lambda a, b: a < b, lambda a, b: a <= b),
            ):
                constraints = []
                for v in range(n):
                    constraints.extend([less(cs[v], min(k, n)), leq(cs[v], v), less(ds[v], n)])
                    constraints.append(z3.Implies(cs[v] != 0,
                        z3.Or([cs[u] == cs[v]-1 for u in range(v)])))
                    constraints.append((ds[v] == 0) == z3.And([cs[u] != cs[v] for u in range(v)]))
                    neighbors = [u for u in range(n) if tuple(sorted((u, v))) in edges]
                    constraints.append(z3.Implies(ds[v] != 0,
                        z3.Or([z3.And(cs[u] == cs[v], less(ds[u], ds[v])) for u in neighbors])))
                formulas.append(z3.And(constraints))
            solver = z3.Solver()
            solver.add(z3.Xor(*formulas))
            assert solver.check() == z3.unsat, (n, k, shape)
            checks += 1
print(f"{checks} full structural formula equivalence checks UNSAT for disagreement; n=1,2,3,4,5,8; empty/path/complete graphs; K=1,n,n+3")
