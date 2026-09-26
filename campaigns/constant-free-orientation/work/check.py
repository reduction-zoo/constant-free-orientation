"""Independent 3-SAT and graph-orientation oracles."""

import argparse
import json
import subprocess
import sys
from itertools import combinations_with_replacement, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target, dict):
        return False
    n, edges = target.get("vertices"), target.get("edges")
    if type(n) is not int or n < 0 or not isinstance(edges, list):
        return False
    degrees = [0] * n
    for edge in edges:
        if not (isinstance(edge, list) and len(edge) == 2 and
                all(type(v) is int and 0 <= v < n for v in edge)):
            return False
        degrees[edge[0]] += 1
        degrees[edge[1]] += 1
    return all(degree in (2, 8) for degree in degrees)


def direct_orientation(target, heads):
    if not legal_target(target) or not isinstance(heads, list) or len(heads) != len(target["edges"]):
        return False
    indegrees = [0] * target["vertices"]
    for edge, head in zip(target["edges"], heads):
        if type(head) is not int or head not in edge:
            return False
        indegrees[head] += 1
    degrees = [0] * target["vertices"]
    for u, v in target["edges"]:
        degrees[u] += 1
        degrees[v] += 1
    return all(indegree in ((0, 2) if degree == 2 else (1, 4))
               for degree, indegree in zip(degrees, indegrees))


def target_solutions(target, limit=3):
    if not legal_target(target):
        raise ValueError("Illegal degree-restricted multigraph")
    n, edges = target["vertices"], target["edges"]
    towards_second = [z3.Bool(f"head_second_{i}") for i in range(len(edges))]
    solver = z3.Solver()
    for i, (u, v) in enumerate(edges):
        if u == v:
            solver.add(towards_second[i] == False)
    degrees = [0] * n
    incoming = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        degrees[u] += 1
        degrees[v] += 1
        if u == v:
            incoming[u].append(z3.IntVal(1))
        else:
            incoming[u].append(z3.If(towards_second[i], 0, 1))
            incoming[v].append(z3.If(towards_second[i], 1, 0))
    for vertex in range(n):
        solver.add(z3.Or(*[z3.Sum(*incoming[vertex]) == value
                           for value in ((0, 2) if degrees[vertex] == 2 else (1, 4))]))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        heads = [v if z3.is_true(model.eval(flag)) else u
                 for (u, v), flag in zip(edges, towards_second)]
        if not direct_orientation(target, heads):
            raise AssertionError("Z3 orientation failed direct validation")
        outputs.append({"heads": heads})
        solver.add(z3.Or(*[flag != model.eval(flag) for flag in towards_second]))
    return outputs or [{"status": "NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target, 1)[0]


def valid_target(target, output):
    if not legal_target(target) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"heads"} and direct_orientation(target, output["heads"])


def exhaustive_target(target):
    if not legal_target(target):
        raise ValueError("Illegal target")
    for choices in product((0, 1), repeat=len(target["edges"])):
        heads = [edge[choice] for edge, choice in zip(target["edges"], choices)]
        if direct_orientation(target, heads):
            return {"heads": heads}
    return {"status": "NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable, str(root / "research/validate_preparation.py"), str(path)], check=True, cwd=root)
    cases = json.loads(path.read_text())
    for n, clauses, answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars": n, "clauses": clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                         for clause in source["clauses"])
                     for bits in product((False, True), repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source, current) and valid_source(source, case["expected"])
    assert not valid_source({"num_vars": 1, "clauses": [[1]]}, {"assignment": [False]})
    test_hand_cases()
    targets = 0
    for n in range(4):
        edge_types = [[u, v] for u in range(n) for v in range(u, n)]
        for m in range(9):
            for indices in combinations_with_replacement(range(len(edge_types)), m):
                target = {"vertices": n, "edges": [edge_types[i] for i in indices]}
                if legal_target(target):
                    assert ("heads" in solve_target(target)) == ("heads" in exhaustive_target(target))
                    targets += 1
    eight_parallel = {"vertices": 2, "edges": [[0, 1]] * 8}
    assert ("heads" in solve_target(eight_parallel)) == ("heads" in exhaustive_target(eight_parallel))
    targets += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {targets} exhaustive target graphs")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable, str(path)], input=json.dumps(source), text=True, capture_output=True, check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal candidate target: {target}")
        for output in target_solutions(target):
            if not valid_target(target, output):
                raise AssertionError(f"Target oracle returned invalid output: {output}")
            payload = {"source": source, "target_solution": output}
            extraction = subprocess.run([sys.executable, str(path), "--extract"], input=json.dumps(payload), text=True, capture_output=True, check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source, recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
