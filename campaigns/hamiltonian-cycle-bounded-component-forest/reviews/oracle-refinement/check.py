"""Check general-K unsigned capacity arithmetic without importing either oracle."""
from itertools import product
import z3

checks = 0
for weights in ([0, 0, 0], [0, 1, 2], [1, 3, 4], [127, 128, 0],
                [255, 1, 0], [2**257, 2**257-1, 1]):
    total = sum(weights)
    width = max(1, total.bit_length())
    for bound in sorted({1, max(1, total//2), max(1, total), total+1, 2**600}):
        for labels in product(range(3), repeat=len(weights)):
            for color in range(3):
                exact = sum(w for w, c in zip(weights, labels) if c == color)
                encoded = sum((z3.If(z3.IntVal(c) == color, z3.BitVecVal(w, width),
                                     z3.BitVecVal(0, width)) for w, c in zip(weights, labels)),
                              z3.BitVecVal(0, width))
                assert z3.simplify(encoded).as_long() == exact
                comparison = z3.ULE(encoded, z3.BitVecVal(min(bound, total), width))
                assert z3.is_true(z3.simplify(comparison)) == (exact <= bound)
                checks += 1
print(f"{checks} exact-sum and capacity comparisons passed; zero totals, unsigned boundary, power-of-two totals, huge bounds and 258-bit weights")
