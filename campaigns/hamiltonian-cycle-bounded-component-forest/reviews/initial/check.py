"""Exhaustive actual-target partitions for triangle and path; no oracle imports."""
import json
from pathlib import Path
import subprocess
import sys

candidate = Path(__file__).resolve().parents[2] / "work/algorithm.py"

def invoke(data, recover=False):
    run = subprocess.run([sys.executable, str(candidate)] + (["--extract"] if recover else []),
                         input=json.dumps(data), text=True, capture_output=True, check=True)
    return json.loads(run.stdout)

def connected(block, edges):
    seen = {block[0]}
    while True:
        new = {v for u, v in edges if u in seen and v in block}
        new |= {u for u, v in edges if v in seen and u in block}
        if new <= seen:
            return seen == set(block)
        seen |= new

for closing in (False, True):
    source = {"vertices": [23, -7, 11], "edges": [[23, -7], [-7, 11]]}
    if closing:
        source["edges"].append([11, 23])
    target = invoke(source)
    weights, edges, bound = target["weights"], target["edges"], target["B"]
    assert target["K"] == 2
    n = len(weights)
    total = sum(weights)
    assert total > bound
    feasible = 0
    # Every two-block partition appears once, fixing vertex zero in the first block.
    for mask in range(1 << (n-1)):
        left = [0] + [i for i in range(1, n) if mask & (1 << (i-1))]
        mass = sum(weights[i] for i in left)
        if mass > bound or total-mass > bound:
            continue
        right = [i for i in range(n) if i not in left]
        if not right or not connected(left, edges) or not connected(right, edges):
            continue
        feasible += 1
        output = {"blocks": [right[::-1], left[::-1]]}
        cycle = invoke({"source": source, "target_solution": output}, True)
        assert sorted(cycle) == sorted(source["vertices"])
        allowed = {frozenset(e) for e in source["edges"]}
        assert all(frozenset((u, v)) in allowed for u, v in zip(cycle, cycle[1:]+cycle[:1]))
    assert feasible == (2 if closing else 0)
    if not feasible:
        assert invoke({"source": source, "target_solution": "NO-SOLUTION"}, True) == "NO-SOLUTION"
    print(f"{'triangle' if closing else 'path'}: {1 << (n-1)} assignments exhausted, {feasible} valid partitions; recovery passed")
