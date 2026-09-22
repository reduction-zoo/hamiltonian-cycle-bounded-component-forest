"""Hamiltonian ordering -> carry-free subset sum -> two anchored blocks."""
import argparse
from itertools import combinations
import json
import sys

sys.set_int_max_str_digits(0)
NO = "NO-SOLUTION"


def validate_source(x):
    vertices, edges = x["vertices"], x["edges"]
    if (not isinstance(vertices,list) or not isinstance(edges,list)
            or not all(type(v) is int for v in vertices) or len(set(vertices)) != len(vertices)):
        raise ValueError("invalid explicit vertices")
    seen = set()
    for edge in edges:
        if (not isinstance(edge,list) or len(edge) != 2
                or not all(type(v) is int and v in vertices for v in edge)
                or edge[0] == edge[1] or tuple(sorted(edge)) in seen):
            raise ValueError("invalid simple graph edge")
        seen.add(tuple(sorted(edge)))


def clauses(x):
    vertices = x["vertices"]
    r = len(vertices)-1
    edges = {tuple(sorted(e)) for e in x["edges"]}
    result = []
    # Variable v*r+p: remaining vertex v occurs in remaining position p.
    groups = [[v*r+p for v in range(r)] for p in range(r)]
    groups += [[v*r+p for p in range(r)] for v in range(r)]
    for group in groups:
        result.append([(i,True) for i in group])
        result.extend([(i,False),(j,False)] for i,j in combinations(group,2))
    for v in range(r):
        if tuple(sorted((vertices[0],vertices[v+1]))) not in edges:
            result.extend([[(v*r,False)],[(v*r+r-1,False)]])
    for p in range(r-1):
        for v in range(r):
            for w in range(r):
                if v != w and tuple(sorted((vertices[v+1],vertices[w+1]))) not in edges:
                    result.append([(v*r+p,False),(w*r+p+1,False)])
    return result


def forward(x):
    n = len(x["vertices"])
    if n < 3:
        return {"weights":[2],"edges":[],"K":1,"B":1}
    cnf = clauses(x)
    variables = (n-1)**2
    ceilings = [1 << (len(c)-1).bit_length() for c in cnf]
    radix = 2*max(ceilings)
    powers = [radix**j for j in range(variables+len(cnf))]
    items = [powers[i] for i in range(variables) for _ in range(2)]
    target = sum(powers[:variables])
    for j, (clause, ceiling) in enumerate(zip(cnf,ceilings)):
        place = powers[variables+j]
        target += ceiling*place
        for i, positive in clause:
            items[2*i + (not positive)] += place
        for bit in range(ceiling.bit_length()-1):
            items.append((1 << bit)*place)
    total = sum(items)
    weights = [total,2*target]+items
    return {"weights":weights,"edges":[[a,i] for i in range(2,len(weights)) for a in (0,1)],
            "K":2,"B":total+target}


def extract(x, out):
    if out == NO:
        return NO
    n = len(x["vertices"])
    if n < 3:
        raise ValueError("small source has only an infeasible target")
    cnf = clauses(x)
    r = n-1
    count = 2+2*r*r+sum((len(c)-1).bit_length() for c in cnf)
    blocks = out["blocks"]
    if (not isinstance(blocks,list) or len(blocks) != 2
            or not all(isinstance(b,list) and b for b in blocks)):
        raise ValueError("invalid target partition shape")
    flat = [v for block in blocks for v in block]
    if not all(type(v) is int for v in flat) or sorted(flat) != list(range(count)):
        raise ValueError("invalid target partition coverage")
    chosen = next(block for block in blocks if 0 in block)
    if 1 in chosen:
        raise ValueError("anchors must be separated")
    cycle = [x["vertices"][0]]
    for p in range(r):
        matches = [v for v in range(r) if 2+2*(v*r+p) in chosen]
        if len(matches) != 1:
            raise ValueError("invalid positional truth choices")
        cycle.append(x["vertices"][1+matches[0]])
    edges = {tuple(sorted(e)) for e in x["edges"]}
    if (len(set(cycle)) != n or
            not all(tuple(sorted((u,v))) in edges for u,v in zip(cycle,cycle[1:]+cycle[:1]))):
        raise ValueError("target output does not decode to a cycle")
    return cycle


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract",action="store_true")
    args = parser.parse_args()
    data = json.load(sys.stdin)
    x = data["source"] if args.extract else data
    validate_source(x)
    result = extract(x,data["target_solution"]) if args.extract else forward(x)
    print(json.dumps(result))
