# 3-SAT → Constant-free graph orientation

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

The target is a graph allowing parallel edges and loops. Degree-eight vertices require indegree in {1,4}; degree-two vertices require indegree in {0,2}. A solution orients every edge subject to these rules, without externally fixed ports.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This tests whether a small uniform orientation constraint can encode Boolean computation without supplied constants.

## Difficulty

The source formulation and constant-forcing mechanism require care; a reduction with preassigned ports does not settle this question.

## Literature context

A reduction that supplies fixed port values would establish a different result. The question here permits only the two stated local indegree rules.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [MIT Hardness Group et al. (2026)](https://arxiv.org/html/2603.03488v1): MIT Hardness Group et al. (2026), Section 3.3, states the orientation case as open. The same passage calls it equivalent to positive {1,4}-in-8 SAT-E2. Section 2 defines SAT without negative literals unless specified. Both claims also appear in the PDF, printed page 20. The inspected abstract history lists only v1. Theorems 3.12 and 3.22 provide the relevant constant-enabled classification and a conditional way to remove constants. They do not supply a terminator for this case.
- [PDF](https://arxiv.org/pdf/2603.03488): MIT Hardness Group et al. (2026), Section 3.3, states the orientation case as open. The same passage calls it equivalent to positive {1,4}-in-8 SAT-E2. Section 2 defines SAT without negative literals unless specified. Both claims also appear in the PDF, printed page 20. The inspected abstract history lists only v1. Theorems 3.12 and 3.22 provide the relevant constant-enabled classification and a conditional way to remove constants. They do not supply a terminator for this case.
- [Even Delta-Matroids and the Complexity of Planar Boolean CSPs](https://arxiv.org/abs/1602.03124): The unrestricted Boolean CSP and counting Holant classifications found in the search do not directly classify this occurrence-restricted decision problem. Even Delta-Matroids and the Complexity of Planar Boolean CSPs gives a tractability theorem for even delta-matroid edge relations. The relation here contains both weights one and four, so it is not even. This observation alone supplies no hardness theorem.

Fixed from board record `website/questions/constant-free-orientation.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
