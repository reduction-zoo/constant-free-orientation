# Research instructions

Read the [fixed question](campaigns/constant-free-orientation/question.md), [prior state](campaigns/constant-free-orientation/state.md) and [preparation notes](campaigns/constant-free-orientation/work/preparation.md). The fixed [test corpus](campaigns/constant-free-orientation/work/cases.json) and [verifier](campaigns/constant-free-orientation/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/constant-free-orientation/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
