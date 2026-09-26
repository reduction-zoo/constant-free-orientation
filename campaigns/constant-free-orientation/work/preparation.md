# Preparation evidence

Prepared on 2026-09-26 before any construction. The fixed corpus contains
120 distinct legal 3-SAT formulas: 20 hand-labelled edge cases and 100 seeded
random cases, with 64 SAT and 56 UNSAT decisions, zero to six variables, and
zero to ten clauses. `generate_cases.py` holds the seeds and generator;
`cases.json` holds independently checked outputs. Z3 4.16.0 encodes each
literal as a Boolean variable or its negation and each clause as a disjunction.
Its SAT models are validated by direct clause evaluation. UNSAT is conclusive;
unknown is an error. Exhaustive Boolean assignments agreed with Z3 on all
120 formulas.

For the target, Z3 assigns each nonloop edge a Boolean head choice and sums
incoming edges at each vertex, enforcing exactly the stated indegree sets.
Loops contribute one to indegree and two to undirected degree. Every feasible
Boolean assignment is a legal orientation, and every legal orientation gives
such an assignment. Returned orientations are checked by a separate direct
degree and indegree count. Exhaustive edge-choice enumeration agreed with Z3
on 38 legal small multigraphs, including degree-eight vertices and loops.
Hand fixtures check a forced pair of parallel edges, a loop obstruction,
four loops at one degree-eight vertex, invalid output and illegal degree.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/constant-free-orientation/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates each random source,
rechecks labels and witnesses, and runs independent target enumeration. The
candidate runner uses separate subprocesses and up to three valid target
orientations per source. An incorrect injected candidate was rejected after
solving its constructed target and validating recovery. No actual reduction
candidate exists. These finite checks do not establish a reduction or hardness.
