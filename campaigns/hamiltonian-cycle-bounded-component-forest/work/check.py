"""Prepared graph oracles and direct validators; no candidate imports."""
import argparse
from itertools import permutations
import json
from pathlib import Path
import subprocess
import sys
import z3

sys.set_int_max_str_digits(0)
NO = "NO-SOLUTION"


def graph_edges(vertices, edges):
    assert all(type(v) is int for v in vertices) and len(set(vertices)) == len(vertices)
    normalized = set()
    for edge in edges:
        assert len(edge) == 2 and all(type(v) is int and v in vertices for v in edge)
        u, v = edge
        assert u != v and tuple(sorted(edge)) not in normalized
        normalized.add(tuple(sorted(edge)))
    return normalized


def source_solutions(x):
    vertices = x["vertices"]
    edges = graph_edges(vertices, x["edges"])
    if len(vertices) < 3:
        return []
    return [[vertices[0], *rest] for rest in permutations(vertices[1:])
            if all(tuple(sorted((u, v))) in edges
                   for u, v in zip((vertices[0], *rest), (*rest, vertices[0])))]


def source_valid(x, out):
    if out == NO:
        return not source_solutions(x)
    return (isinstance(out, list) and len(out) >= 3 and all(type(v) is int for v in out)
            and sorted(out) == sorted(x["vertices"])
            and all(tuple(sorted((u,v))) in graph_edges(x["vertices"], x["edges"])
                    for u,v in zip(out, out[1:]+out[:1])))


def connected(block, edges):
    seen = {block[0]}
    while True:
        added = {v for u,v in edges if u in seen and v in block}
        added |= {u for u,v in edges if v in seen and u in block}
        if added <= seen:
            return seen == set(block)
        seen |= added


def target_valid(t, out):
    n = len(t["weights"])
    edges = graph_edges(list(range(n)), t["edges"])
    if out == NO:
        return target_solutions(t, limit=1) == [NO]
    if not isinstance(out, dict) or not isinstance(out.get("blocks"), list):
        return False
    blocks = out["blocks"]
    if len(blocks) > t["K"] or not all(isinstance(b,list) and b for b in blocks):
        return False
    flat = [v for block in blocks for v in block]
    if not all(type(v) is int for v in flat) or sorted(flat) != list(range(n)):
        return False
    if not all(sum(t["weights"][v] for v in b) <= t["B"] and connected(b, edges) for b in blocks):
        return False
    if "trees" in out:
        trees = out["trees"]
        if not isinstance(trees, list) or len(trees) != len(blocks):
            return False
        for block, tree in zip(blocks, trees):
            if not isinstance(tree, list) or len(tree) != len(block)-1:
                return False
            if not all(isinstance(e,list) and len(e)==2 and
                       all(type(v) is int and v in block for v in e) and
                       tuple(sorted(e)) in edges for e in tree):
                return False
            if len({tuple(sorted(e)) for e in tree}) != len(tree) or not connected(block, tree):
                return False
    return True


def target_solutions(t, limit=12):
    weights, K, B = t["weights"], t["K"], t["B"]
    assert type(K) is int and K > 0 and type(B) is int and B > 0
    assert all(type(w) is int and w >= 0 for w in weights)
    n = len(weights)
    edges = graph_edges(list(range(n)), t["edges"])
    if n == 0:
        return [{"blocks":[]}]
    solver = z3.Solver()
    colors = [z3.Int(f"c{v}") for v in range(n)]
    depths = [z3.Int(f"d{v}") for v in range(n)]
    for v in range(n):
        solver.add(colors[v] >= 0, colors[v] < min(K,n), colors[v] <= v,
                   depths[v] >= 0, depths[v] < n)
        solver.add(z3.Implies(colors[v] > 0,
                             z3.Or([colors[u] == colors[v]-1 for u in range(v)])))
        root = z3.And([colors[v] != colors[u] for u in range(v)])
        solver.add((depths[v] == 0) == root)
        neighbors = [u for u in range(n) if tuple(sorted((u,v))) in edges]
        solver.add(z3.Implies(depths[v] > 0,
                             z3.Or([z3.And(colors[u] == colors[v], depths[u] < depths[v])
                                    for u in neighbors])))
    for c in range(min(K,n)):
        solver.add(z3.Sum([z3.If(colors[v] == c, weights[v], 0) for v in range(n)]) <= B)
    outputs = []
    while len(outputs) < limit:
        status = solver.check()
        if status == z3.unknown:
            raise RuntimeError(solver.reason_unknown())
        if status == z3.unsat:
            return outputs or [NO]
        model = solver.model()
        labels = [model.eval(c).as_long() for c in colors]
        out = {"blocks":[[v for v in range(n) if labels[v]==c] for c in range(max(labels)+1)]}
        assert target_valid(t, out)
        outputs.append(out)
        solver.add(z3.Or([colors[v] != labels[v] for v in range(n)]))
    return outputs


def invoke(path, data, extract=False):
    result = subprocess.run([sys.executable,str(path)]+(["--extract"] if extract else []),
                            input=json.dumps(data),text=True,capture_output=True,check=True)
    return json.loads(result.stdout)


def fixtures():
    return json.loads(Path(__file__).with_name("cases.json").read_text())


def self_test():
    for case in fixtures():
        x = case["source"]
        solutions = source_solutions(x)
        assert bool(solutions) == case["yes"]
        assert source_valid(x, solutions[0] if solutions else NO)
        assert not source_valid(x, NO if solutions else x["vertices"])
    targets = [
        ({"weights":[],"edges":[],"K":1,"B":1}, 1),
        ({"weights":[0,0],"edges":[],"K":1,"B":1}, 0),
        ({"weights":[0,0],"edges":[],"K":2,"B":1}, 1),
        ({"weights":[1,1],"edges":[[0,1]],"K":2,"B":2}, 2),
        ({"weights":[2],"edges":[],"K":3,"B":1}, 0),
        ({"weights":[1,1,1],"edges":[[0,1],[1,2]],"K":2,"B":2}, 2),
        ({"weights":[10**5000,0],"edges":[[0,1]],"K":1,"B":10**5000}, 1),
    ]
    for t, count in targets:
        outputs = target_solutions(t)
        assert (0 if outputs == [NO] else len(outputs)) == count
        assert all(target_valid(t,out) for out in outputs)
    path = targets[5][0]
    assert not target_valid(path,{"blocks":[[0,2],[1]]})
    assert not target_valid(path,{"blocks":[[0,1,2]]})
    assert not target_valid(path,{"blocks":[[0,1],[1,2]]})
    assert not target_valid(path,{"blocks":[[0],[1],[2]]})
    assert target_valid(path,{"blocks":[[0,1],[2]],"trees":[[[0,1]],[]]})
    assert not target_valid(path,{"blocks":[[0,1],[2]],"trees":[[],[]]})
    print(f"self-test: {len(fixtures())} source fixtures, {len(targets)} target fixtures; invalid connectivity, coverage, weight, block count and trees rejected")


def candidate(path):
    count = 0
    for case in fixtures():
        t = invoke(path,case["source"])
        outputs = target_solutions(t)
        for out in outputs:
            recovered = invoke(path,{"source":case["source"],"target_solution":out},True)
            assert source_valid(case["source"],recovered), (case["name"],out,recovered)
            count += 1
        print(f"{case['name']}: {len(outputs)} valid target outputs; recovery passed",flush=True)
    print(f"candidate: {len(fixtures())} instances; {count} recoveries passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    self_test() if args.self_test else candidate(args.candidate)
