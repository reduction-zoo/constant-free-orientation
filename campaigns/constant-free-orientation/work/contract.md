# Prepared input and output contract

The 3-SAT source input is `{"num_vars": n, "clauses": [[signed_literals],
...]}` with `n >= 0`, at most three literals per clause, and each nonzero
literal's absolute value at most `n`. Empty and repeated clauses or literals
are legal. A source output is `{"assignment": [bool, ...]}` satisfying every
clause, or `{"status": "NO-SOLUTION"}` exactly when none exists.

The target input is `{"vertices": n, "edges": [[u, v], ...]}`. Parallel edges
and loops are legal. Each edge endpoint is an integer vertex in `0..n-1`.
Every vertex has undirected degree two or eight, with a loop contributing two
to degree. A target output is `{"heads": [vertex, ...]}`, one endpoint chosen
as the head of each edge. A loop contributes one to its vertex's indegree.
Degree-two vertices require indegree zero or two; degree-eight vertices require
indegree one or four. `{"status": "NO-SOLUTION"}` is valid exactly when no
orientation satisfies all rules. The empty graph has an empty orientation.

A candidate `algorithm.py` reads a source JSON object from stdin and writes a
legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. Errors exit nonzero and diagnostics go to stderr. Forward and recovery
are separate processes. The candidate must be deterministic and polynomial
time, and recovery must work for every valid target output.

`check.py --candidate PATH` independently solves each constructed target on
the fixed source corpus and directly validates each recovered source output.
