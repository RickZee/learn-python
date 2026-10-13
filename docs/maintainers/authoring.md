[Home](../../README.md) › [Maintainers](README.md) › Authoring

# Authoring rules

Read this only when you are authoring the course (see `AGENTS.md`). Locked decisions D1–D4, D7–D9 from round 5 are included below.

## Layout
- course/: the language course. NN-topic/NN-name-lesson.ipynb plus NN-name-practice.ipynb. Part 2 units add an exercise/ folder (.py stubs plus test_*.py).
- internals/: how Python works (objects, dicts, GIL, …), linked from course Why sections.
- patterns/: algorithm patterns, each taught on a sibling problem, not a challenges problem.
- challenges/: guide.ipynb, problems/, codebase-rounds/, python-questions.md.
- use-cases/: projects and explore pages.
- solutions/: reference solutions at the mirrored path. Challenge notebooks may link only to their own walkthrough, and only under `## After you pass`. Never link to solutions from other learner files.
- src/pylearn/: check() and load_exercise().
- tests/ and tools/: the harness. Maintainer notes live in `docs/maintainers/review/` (stub at `review/README.md`).

## Commands
- Setup: uv sync
- All checks: uv run pytest -n auto && uv run ruff check .
- Part 2 and projects against solutions: PYLEARN_SOLUTIONS=1 uv run pytest course use-cases
- Refresh notebook outputs: uv run python tools/refresh_outputs.py <paths>

## Authoring standards
- Never type notebook outputs. Execute with tools/refresh_outputs.py.
- Every practice exercise has a reference solution under solutions/ at the mirrored path. Run the checks before finishing.
- Practice stubs use `raise NotImplementedError`. Checks use `pylearn.check`, or `assert ..., "message"`.
- Never put a solution in a learner-facing file. Hints go in collapsed <details> blocks, ordered from concept to approach to near-code.
- Don't use a concept before the lesson that introduces it (docs/maintainers/concepts.md). Rewrite the exercise instead.
- Loops come before collections. `for` over `range` and strings is taught before lists and dicts. After that, unrolled code written to avoid a loop is banned.
- course/ and patterns/ use the standard library only.
- Common mistakes are real mistakes. Show the bug learners actually make in that topic. If it raises, tag the cell `raises-exception`. If it is silent, print the wrong result, then show the fix in the next cell with a sentence explaining why it was wrong. Banned: one-liners whose only point is that an error exists (`print([1][3])`, `None.value`, `[].pop()`).
- Every lesson explains why. Every lesson gets two sections:
  - `## Why it works this way`: the mechanism underneath, what it costs (time and memory), and the design reason. Link the matching `internals/` lesson.
  - `## When to use it`: when this is the right tool, when it isn't, and what to use instead.
  A "why" answer must not just restate the fact.
- Depth scales with difficulty. Tag every lesson in its first cell as **Core**, **Intermediate**, or **Deep**. Target words, excluding code: Core 350–600, Intermediate 600–1,000, Deep 900–1,600 with a diagram or trace table. Deep covers generators, decorators, the data model, concurrency, async, every pattern lesson, and every `internals/` lesson. Don't pad. If a lesson needs more than that, split it.
- Pattern lessons fully solve a sibling problem. The worked example is a complete, realistic solution to a problem that is not in `challenges/problems/`, followed from start to end. Banned: placeholder functions and the phrase "not the practice problem". Pattern lessons and practice must not solve any problem in `challenges/problems/`.
- Prerequisites are links. `**Uses:**` must be Markdown links to the lessons it builds on, or `**Uses:** nothing yet`, so `tests/test_links.py` checks them.
- Facts get checked by running them. Any claim about behaviour must be backed by a cell that prints the evidence. CPython-only details are labelled "CPython detail" and tagged `volatile` if the output can vary.
- A notebook cell meant to error is tagged `raises-exception`. Machine-dependent output is tagged `volatile`.
- `asyncio.run` never appears in a notebook; use top-level await. Code that must run as a program goes in a .py file run with subprocess or pytest.
- Voice: short, plain, declarative sentences. Define a term the first time you use it. No Python version numbers in learner-facing text.
- Moves use git mv. Afterwards tests/test_links.py must pass.

### Locked decisions (round 5)

- **D1. No reference implementations in learner files.** Random cross-checks call `pylearn.challenges.cross_check(slug, func)`. Each oracle is slow by construction: it tries every option, uses no memo, no DP table, no clever data structure, and runs only on small inputs. It must not match the reference solution's normalized AST. Property checks stay in the notebook. Design problems use `cross_check_ops` against a slow model in `pylearn.challenges`.
- **D2. Challenge walkthrough links.** Challenge notebooks may link only to their own walkthrough, and only under `## After you pass`. No "Solutions:" line in the first cell.
- **D3. Every assert must test something.** An assert whose test is a constant, or compares only constants, is banned everywhere. A challenge's check count counts only asserts that call the function or class under test, plus one for a `cross_check(...)` call.
- **D4. A hint never contains the answer.** The last hint ("near the code") is a skeleton with `___` blanks, or at most one line of the solution. It never includes a whole function body.
- **D7. Guards normalize before they match.** Every banned-phrase check lowercases the text, turns `-` and `_` into spaces, and collapses whitespace before matching. Repetition thresholds are more than two notebooks.
- **D8. Projects are milestones.** Each project has 4–6 milestones. Each milestone has its own test file, `tests/test_m<N>_<name>.py`, and its own README section. A learner runs `uv run pytest <project> -k m1`, then `-k m2`, and so on.
- **D9. Practice has a Debug item.** The practice order is Warm-up → Core → Debug → Stretch → Reflect. Debug is a short function with the lesson's common mistake planted in it, plus checks that fail until it's fixed. Required from `course/02-strings` onward.

## Lesson flow

Every course and internals lesson follows this order. Teach first; questions come after. Predicting code output is a check after the explanation, not the opening move. No goal may start with "predict", and no `## Predict` heading may remain.

1. **First cell.** Title and tier, then:
   - **Why you'd use this:** a real situation in 2–4 plain sentences.
   - **After this lesson you can:** 2–3 plain-language goals tied to that situation. Never start a goal with "predict".
   - Time, and **Uses:** links.
2. `## Quick review`: 2–3 short questions on earlier lessons (spaced retrieval), answers in `<details>`. Omit only in the first lesson of the course.
3. `## The idea`: the explanation, with a concrete analogy, plus the existing "Explain more" layer.
4. `## See it work`: the worked example solving the situation from cell 1, with labelled steps.
5. `## Check yourself`: 2–4 quick questions on code like the example, answers in `<details><summary>Check your answers</summary>`.
6. `## Why it works this way` and `## When to use it` (mechanism, cost, design reason; when this tool fits and what to use instead).
7. `## Common mistake` (a real mistake learners make in this topic).
8. `## Try it`: change the example to do something new.
9. `## Recap`, then `**Next:**` the practice.

Practice notebooks: Warm-up → Core → Debug → Stretch → Reflect. The stretch is a small realistic task, not a puzzle. Debug is required from `course/02-strings` onward (D9).

Pattern lessons keep their 9-part structure (Recognize it through Python idioms), with the same first cell (why you'd use it, plain goals) and a `## Quick review` before "Recognize it".

`docs/maintainers/status.md` tracks pending guard paths; that list only shrinks.

**Next:** [Concept ledger](concepts.md)
