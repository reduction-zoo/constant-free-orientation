# constant-free-orientation

Standalone formal definition of Q010. `record.json` preserves the exact
board source, target, requested result and equation used for this definition.
`Challenge.lean` imports only Mathlib. `Solution.lean` is its identical starting
copy, with the open theorem deliberately unproved.

## Modelling choices

SAT clauses have at most three signed literal occurrences; empty clauses and repeated literals are allowed. Variables are zero based and assignments have exactly the declared length. All finite structures and all witness data are explicitly encoded. Parallel edges and loops are retained. A loop contributes two to degree and one to indegree. A head endpoint is supplied per edge; no externally fixed ports are admitted.

Graphs explicitly encode all vertex labels, including isolated vertices, so their bit length is at least their vertex count. Finite indices are zero based. Numerical data use Q001's self-delimiting binary
encoding unless the source explicitly requires unary. `none` means no valid
witness exists; it never means a program error. Construction and recovery must
be deterministic polynomial-time TM2 computations with polynomial output bounds,
as in Q001. Recovery is universal over valid target outputs and receives the
original source instance as well. Legal-instance predicates are specifications,
not algorithms the proposed reduction must execute.

The prepared contract restricts every vertex to degree two or eight; the formal legal-instance predicate follows that restriction. SEMANTIC REVIEW: the short board text states only the two local rules, so confirm it intends this degree promise rather than unconstrained vertices of other degrees.

## Build and verification

Lean 4.35.0 and matching Mathlib are pinned by `lean-toolchain`, `lakefile.toml`
and `lake-manifest.json`. In this directory run:

```sh
lake exe cache get Mathlib.Computability.TuringMachine.Computable
LEAN_NUM_THREADS=2 lake build
lake env lean Audit.lean
./scripts/verify-comparator.sh
```

The comparator script and repository-root Linux CI follow the pinned Q001
reference. They run the bundled `lake comparator` with the strict axiom policy,
then, for an unfilled solution, require full statement agreement and rejection
only for `sorryAx`. Green CI verifies an open template, not a completed proof.
The script needs Linux and bubblewrap; macOS compilation is not comparator
verification. `Tests.lean` checks finite boundary examples, not general semantic
equivalence. Human review of the problem statement remains necessary.

## Provenance and license

Infrastructure follows Q001 at `6e5d9d7aa425db5f01ee44f4c4e1710cf2993fda`.
The files in this formal project are licensed under Apache-2.0; see `LICENSE`.
This does not change licensing of other files in the research repository.

### Reference encoding limitation

As in Q001, a formula declares its variable count in binary while a search assignment explicitly lists every variable, including unused variables. Thus this encoding is not polynomially balanced when the count is large and most variables are unused. The theorem retains Q001's stated runtime measure for recovery (the full source/target-output pair); this is not a separate proof that the usual explicit-variable complexity formulation is equivalent. Review this convention before making a hardness claim.

Local verification results are recorded in `evidence/statement/verification.json`.
The comparator prerequisite test passes on macOS; its real Linux verdict cases
are skipped, and the comparator script itself exits at the missing `bwrap` prerequisite.
