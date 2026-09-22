"""Independent two-block oracle: exact unsigned sums and connectivity filtering."""
import argparse
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import sys
import z3

sys.set_int_max_str_digits(0)
NO = "NO-SOLUTION"


def tree_for(block, edges):
    reached = {block[0]}
    tree = []
    while len(reached) < len(block):
        edge = next(((u,v) for u,v in edges if
                     (u in reached and v in block and v not in reached) or
                     (v in reached and u in block and u not in reached)), None)
        if edge is None:
            return None
        tree.append(list(edge))
        reached.update(edge)
    return tree


def target_solutions(t):
    weights, edges, K, B = t["weights"], t["edges"], t["K"], t["B"]
    n = len(weights)
    assert K in (1,2) and type(B) is int and B > 0
    assert all(type(w) is int and w >= 0 for w in weights)
    assert all(len(e)==2 and all(type(v) is int and 0<=v<n for v in e) and e[0]!=e[1] for e in edges)
    assert len({tuple(sorted(e)) for e in edges}) == len(edges)
    if n == 0:
        return [{"blocks":[]}]
    if K == 1:
        block = list(range(n))
        return [{"blocks":[block]}] if sum(weights)<=B and tree_for(block,edges) is not None else [NO]
    total = sum(weights)
    width = max(1,total.bit_length())
    bound = z3.BitVecVal(min(B,total),width)
    zero = z3.BitVecVal(0,width)
    members = [z3.Bool(f"member_{i}") for i in range(n)]
    solver = z3.SolverFor("QF_BV")
    solver.add(members[0])  # block-order symmetry, not a construction premise
    left = sum((z3.If(v,z3.BitVecVal(w,width),zero) for v,w in zip(members,weights)),zero)
    right = sum((z3.If(v,zero,z3.BitVecVal(w,width)) for v,w in zip(members,weights)),zero)
    solver.add(z3.ULE(left,bound),z3.ULE(right,bound))
    outputs = []
    while len(outputs) < 12:
        result = solver.check()
        if result == z3.unknown:
            raise RuntimeError(solver.reason_unknown())
        if result == z3.unsat:
            return outputs or [NO]
        model = solver.model()
        chosen = [z3.is_true(model.eval(v,model_completion=True)) for v in members]
        blocks = [[i for i in range(n) if chosen[i]==side] for side in (True,False)]
        blocks = [block for block in blocks if block]
        solver.add(z3.Or([v != b for v,b in zip(members,chosen)]))
        if any(tree_for(block,edges) is None for block in blocks):
            continue
        assert sorted(v for block in blocks for v in block) == list(range(n))
        assert all(sum(weights[v] for v in block) <= B for block in blocks)
        outputs.append({"blocks":blocks})
    return outputs


def invoke(path,data,extract=False):
    result = subprocess.run([sys.executable,str(path)]+(["--extract"] if extract else []),
                            input=json.dumps(data),text=True,capture_output=True,check=True)
    return json.loads(result.stdout)


def cases():
    for n in range(5):
        possible = list(combinations(range(n),2))
        for mask in range(1 << len(possible)):
            yield f"all-{n}-{mask}", {"vertices":list(range(n)),
                     "edges":[list(e) for i,e in enumerate(possible) if mask & (1 << i)]}
    yield "cycle-five", {"vertices":list(range(5)),"edges":[[i,(i+1)%5] for i in range(5)]}
    yield "articulation-five", {"vertices":list(range(5)),"edges":[[0,1],[1,2],[2,0],[0,3],[3,4],[4,0]]}
    huge = 10**5000+7
    for yes in (False,True):
        labels = [-huge,0,huge]
        yield "huge-labels", {"vertices":labels,"edges":[[labels[0],0],[0,labels[2]]]+([[labels[0],labels[2]]] if yes else [])}


def run(path):
    counts = dict(instances=0,yes=0,no=0,target_outputs=0,recoveries=0,
                  max_target_vertices=0,max_weight_bits=0,max_capacity_bits=0)
    for name,x in cases():
        vertices = x["vertices"]
        edges = {tuple(sorted(e)) for e in x["edges"]}
        cycles = [] if len(vertices)<3 else [list(p) for p in permutations(vertices)
                     if all(tuple(sorted((u,v))) in edges for u,v in zip(p,p[1:]+p[:1]))]
        t = invoke(path,x)
        counts["max_target_vertices"] = max(counts["max_target_vertices"],len(t["weights"]))
        counts["max_weight_bits"] = max(counts["max_weight_bits"],max(t["weights"],default=0).bit_length())
        counts["max_capacity_bits"] = max(counts["max_capacity_bits"],t["B"].bit_length())
        outputs = target_solutions(t)
        for out in outputs:
            variants = [out]
            if out != NO:
                blocks = [list(reversed(block)) for block in reversed(out["blocks"])]
                variants.append({"blocks":blocks,"trees":[tree_for(block,t["edges"]) for block in blocks]})
            for encoded in variants:
                recovered = invoke(path,{"source":x,"target_solution":encoded},True)
                if not (recovered in cycles if cycles else recovered == NO):
                    raise AssertionError(json.dumps(dict(name=name,source=x,target=t,
                                            target_solution=encoded,recovered=recovered)))
                counts["recoveries"] += 1
        counts["instances"] += 1
        counts["yes" if cycles else "no"] += 1
        counts["target_outputs"] += len(outputs)
        print(f"{name}: {len(outputs)} target outputs; passed",flush=True)
    print(json.dumps(counts,sort_keys=True))
    print("Deterministic finite domain; up to 12 target partitions per instance; exact bit-vector sums cannot overflow; no timeouts.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate",type=Path,required=True)
    run(parser.parse_args().candidate)
