# Agent plan: fix and upgrade the learn-python repo

This plan is written for a coding agent: Cursor's agent, Claude Code (in a terminal, or as the extension inside Cursor or VS Code), or any agent that reads `AGENTS.md`. The reasons behind each step are in [CRITIQUE.md](CRITIQUE.md). The defect numbers (#1, #2, …) refer to its table.

**How to run it.** Do one phase per agent session and one branch per phase. Start each session with:

> Read `review/CRITIQUE.md` and `review/AGENT_PLAN.md`. Do **Phase N** only. Follow the ground rules. When done, run the phase's acceptance checks, show me the results and a summary of the diff, and stop.

In Claude Code, run authoring sessions with a plain `claude`, not the learner profile from Phase 0.9. The learner profile blocks edits to practice files on purpose.

Phases 0–2 are mechanical and safe to run back to back. Phases 3–7 change teaching content, so review each one before starting the next.

---

## Ground rules (apply to every phase)

1. **Never type a notebook output by hand.** Outputs come only from execution: `uv run python tools/refresh_outputs.py <paths>`.
2. **Every practice exercise has a reference solution** under `solutions/` (same relative path; see Phase 2), and `uv run pytest` passes before you say a phase is done.
3. **No solutions in learner-facing files.** Hints go in collapsed `<details>` blocks. Solutions live only in `solutions/`.
4. **No concept before its lesson.** Code in a lesson or practice may only use concepts introduced at or before that point (`docs/concepts.md`, Phase 4). If you need a construct early, rewrite the exercise.
5. **Standard library only in `course/` and `patterns/`.** Third-party packages are allowed in `use-cases/` projects, added with `uv add --group <name>`.
6. **Voice.** Keep the repo's style: short declarative sentences, plain words, and each term defined the first time it appears. Address the learner as "you".
7. **No Python version numbers inside notebooks or lesson text.** The version lives in `.python-version` and `pyproject.toml`.
8. **Moves use `git mv`.** Update every link afterwards; `tests/test_links.py` must pass.
9. **Notebook hygiene.** nbformat 4.5, kernelspec `python3`, every cell has an `id`. Practice notebooks are saved without outputs; lessons are saved with outputs.
10. **Leave `review/` alone.** Don't edit or delete it.
11. **Small commits.** Commit one logical change at a time, with a message that names the defect (e.g. `fix(#1): even_squares expected value`).

---

## Phase 0: Baseline and reproducible setup

**Goal:** a fresh clone sets itself up with one command, and every AI tool a learner might use (Cursor, Claude Code, the Claude app) gets the same standing instructions.

0.1 **Snapshot.** On `main`, commit the current tree as is: `git add -A && git commit -m "Snapshot before review fixes"`. Then `git switch -c review/phase-0`. Most of the repo is untracked today (#13), so do this before anything else.

0.2 **Create `pyproject.toml`** (Appendix A). It sets `requires-python = ">=3.12"` (nothing in the content needs 3.14, see #15), declares dev tools in a `dev` dependency group, and installs a tiny helper package `pylearn` from `src/`.

0.3 **Create `.python-version`** containing `3.14`. 3.15.0 shipped 2026-10-09. Stay on 3.14 for now, because third-party wheels used by the use-case projects lag new releases. CI also tests 3.15.

0.4 **Create `src/pylearn/__init__.py` and `src/pylearn/check.py`** (Appendix B).

0.5 **Run `uv sync`**, then commit `uv.lock`. Leave `.gitignore` as is: it already ignores `.venv`, and `uv.lock` is not ignored.

0.6 **Rewrite `docs/setup.md`:**
- Install uv (link to the official installer page).
- `git clone …`, `cd learn-python`, `uv sync`.
- **Pick an editor**, with one short subsection each:
  - **Cursor or VS Code:** open a notebook, then **Select Kernel → Python Environments → `.venv`**.
  - **JupyterLab:** run `uv run --with jupyter jupyter lab`.
  - **Claude Code users:** notebooks still open in one of the editors above. Claude Code runs in the terminal or as the extension inside Cursor or VS Code. Link to `docs/ai.md`.
- First-run check: a cell with `import pylearn` runs without error.
- **Troubleshooting** for: `ModuleNotFoundError: No module named 'pylearn'` (wrong kernel); conda or Homebrew Python first on `PATH`; how to run the checks (`uv run pytest`).
- Remove the claim that older kernels "reject newer syntax".

0.7 **Strip version text from notebooks.** In every notebook's first Markdown cell, delete the sentence that starts `Select the project \`.venv\` kernel (Python 3.14)`. Replace it with nothing; setup covers it. In `challenges/guide.ipynb`, delete "Use the `.venv` kernel in this folder (Python 3.14)." Do this with a small script that edits cell sources via `nbformat`. Don't hand-edit 150 files.

0.8 **Fix the README:**
- Remove the sentences about `scratch/basics.py` and `archive/learn.ipynb` (#17).
- Remove "Python **3.14**".
- Add a **Who this is for** section with this placeholder text (Rick will edit it): "Primary: people who can already program a little, or in another language, and want fluent, idiomatic Python plus challenge readiness. Beginners: start with `docs/paths/beginner.md`."
- Link to `docs/setup.md` as step 1.

0.9 **AI instructions for every tool.** Keep one source of truth for each of the two modes, authoring and learning. The two must not mix: a tutor that won't touch practice files would block the agent doing Phases 1–7.

**Authoring (Appendix G).** This is how an agent should edit the repo.
- `AGENTS.md` at the repo root holds the repo map, commands, and authoring standards. Cursor reads `AGENTS.md` natively, and so does Claude Code when no `CLAUDE.md` exists.
- `CLAUDE.md` contains `@AGENTS.md` plus a few Claude Code notes, so every Claude Code version and setting loads it.
- No separate authoring `.mdc` file is needed.

**Learning (Appendix H).** This is how an AI should help someone doing the exercises. The canonical text lives in `docs/ai/tutor-prompt.md`, and each tool gets a thin wrapper that includes it word for word:
- **Cursor:** `.cursor/rules/practice-tutor.mdc`, set to *Apply Intelligently* (description only, no globs, so it doesn't fire while authoring). Learners can also `@practice-tutor` it.
- **Claude Code:** a custom output style `.claude/output-styles/python-tutor.md`, plus a learner profile `.claude/learner-settings.json`. The profile turns that style on and denies Claude edits to practice files and reads of `solutions/`. Learners start with `claude --settings .claude/learner-settings.json`. For use-case projects, recommend Claude Code's built-in **Learning** output style (`/output-style learning`), which leaves `TODO(human)` sections for the learner to write.
- **Claude app (web, desktop, mobile):** `docs/ai/claude-project-instructions.md`, to paste into a Claude Project's instructions, plus advice to pick the built-in **Learning** style in the style menu.
- **Sync test:** `tests/test_ai_instructions.py` asserts that each wrapper contains the canonical tutor text verbatim, so they can't drift.

**Learner page.** `docs/ai.md` explains the three ways to use AI here:
- **Learn:** tutor mode, for practice and challenge problems.
- **Build:** the Learning style, for projects.
- **Author:** the default mode, for changing the course.

It gives the steps for Cursor, Claude Code, the Claude app, and "anything else" (paste `docs/ai/tutor-prompt.md` as instructions). It also says to turn off inline autocomplete (Cursor Tab, Copilot) while practising, because instructions don't govern autocomplete.

**Acceptance**
- `rm -rf .venv && uv sync && uv run python -c "import pylearn; print('ok')"` prints `ok`.
- `grep -rl "3\.14" --include=*.ipynb course challenge use-cases` prints nothing.
- `git status` is clean after committing.
- `uv run pytest tests/test_ai_instructions.py` passes, so all tutor wrappers match the canonical text.
- In Cursor and in plain `claude`, an agent asked to "fix the stub in `course/07-comprehensions/01-comprehensions-practice.ipynb`" edits it, so authoring isn't blocked. Under `claude --settings .claude/learner-settings.json`, the same request is refused.

---

## Phase 1: Correctness fixes

**Goal:** nothing in the repo is wrong.

1.1 **#1** `course/07-comprehensions/01-comprehensions-practice.ipynb`: change `assert even_squares(3) == [0]` to `assert even_squares(3) == [0, 4]`.

1.2 **#2** `challenges/problems/14-merge-two-sorted-lists.ipynb`: change the expected value to `[1, 1, 2, 3, 4, 4]`. Add `assert values(mergeTwoLists(nodes([]), nodes([]))) == []`.

1.3 **#3 Async lesson.** Replace the code in `course/23-concurrency/03-async-lesson.ipynb` with the two cells below. Set the Markdown to: "A notebook already runs an event loop, so you `await` at the top level of a cell. A `.py` script has no loop running, so it starts one with `asyncio.run(main())`. `asyncio.run` inside a notebook raises `RuntimeError`." Tag the first cell `volatile` because it prints a timing.

```python
import asyncio
import time


async def fetch(name: str, seconds: float) -> str:
    await asyncio.sleep(seconds)  # stands in for a network call
    return f"{name} done"


start = time.perf_counter()
results = await asyncio.gather(fetch("a", 0.2), fetch("b", 0.2), fetch("c", 0.2))
print(results)
print(f"took {time.perf_counter() - start:.1f}s, not 0.6s")
```

```python
import subprocess
import sys

script = """
import asyncio

async def main():
    await asyncio.sleep(0)
    print("asyncio.run works in a script")

asyncio.run(main())
"""
print(subprocess.run([sys.executable, "-c", script], capture_output=True, text=True).stdout)
```

1.4 **#3 Async practice.** Replace the practice with a task that only passes when the coroutines actually run concurrently. The `fetch` helper is given. Only `fetch_all` is the exercise. Solution body: `return list(await asyncio.gather(*(fetch(name) for name in names)))`.

```python
import asyncio
import time


async def fetch(name: str, seconds: float = 0.2) -> str:
    await asyncio.sleep(seconds)
    return name.upper()


async def fetch_all(names: list[str]) -> list[str]:
    """Fetch every name at the same time. Keep the input order."""
    raise NotImplementedError


start = time.perf_counter()
got = await fetch_all(["a", "b", "c", "d", "e"])
elapsed = time.perf_counter() - start
assert got == ["A", "B", "C", "D", "E"], f"got {got!r}"
assert elapsed < 0.5, f"took {elapsed:.2f}s; the fetches ran one after another"
print("✓ concurrent and in order")
```

1.5 **#4/#5 Modules lesson.**
- Add a real file `course/21-modules/greet.py` (below).
- Rewrite `02-main-lesson.ipynb` to:
  1. print the file,
  2. `import greet` (it shows `module name is greet`, and the guarded block does **not** run),
  3. run it as a program with `subprocess.run([sys.executable, "greet.py"], capture_output=True, text=True)` (it shows `module name is __main__` and `hello world`).
- Explain in the Markdown that inside a notebook `__name__` is always `"__main__"`, which is why the lesson uses a real file.

```python
def greet(name: str) -> str:
    return f"hello {name}"


print("module name is", __name__)

if __name__ == "__main__":
    print(greet("world"))
```

1.6 **#5 Modules practice.** Replace `02-main-practice.ipynb` with an exercise folder `course/21-modules/exercise/`:
- `tool.py`: a learner stub. It defines `main()`, which prints `hello from tool`, and calls `main()` at module level **without** a guard. That's the bug to fix.
- `test_tool.py`: uses `pylearn.load_exercise`. One test asserts that importing prints nothing (`capsys`). Another runs `subprocess.run([sys.executable, tool.__file__], …)` and expects `hello from tool`.
- `solutions/course/21-modules/exercise/tool.py`: the guarded version.
- Delete `02-main-practice.ipynb`. The practice harness expects every `*-practice.ipynb` to fail unsolved, so a Markdown-only notebook would break it. End the lesson's Recap with: "Practice: fix `exercise/tool.py`, then run `uv run pytest course/21-modules/exercise`."
- Verify with `PYLEARN_SOLUTIONS=1 uv run pytest course/21-modules/exercise` (passes) and `uv run pytest course/21-modules/exercise` (fails).

1.7 **#6 Parentheses lesson.** Replace the code cell in `course/15-stacks/01-parentheses-lesson.ipynb` with:

```python
pairs = {")": "(", "]": "[", "}": "{"}


def trace(s: str) -> bool:
    stack = []
    for character in s:
        if character in "([{":
            stack.append(character)  # 1. An opener waits on the stack.
        elif not stack or stack.pop() != pairs[character]:
            print(f"{s!r}: {character!r} has no matching opener")
            return False  # 2. A closer must match the opener on top.
        print(f"  {character!r} -> {stack}")
    print(f"{s!r}: left open {stack}" if stack else f"{s!r}: balanced")
    return not stack  # 3. Nothing may be left open at the end.


for text in ["([]{})", "(]", ")", "(("]:
    trace(text)
```

1.8 **#7 Quick sequencing patch** (Phase 4 does the full fix):
- `01-basics/01-names-practice`: expect `"NoneType"` instead of `"none"`, so `type(value).__name__` solves it.
- `01-basics/03-booleans-practice`: replace `describe` with three exercises that return a bool expression and need no `if`: `is_missing(value)` (`value is None`), `is_negative(n)` (`n < 0`), and `in_range(n, low, high)` (`low <= n <= high`). Phase 3 replaces this again with the full conditions unit.

1.9 **Low-severity items (#18):**
- `04-control-flow/03-zip-lesson`: add `zip(a, b, strict=True)` and show the `ValueError` it raises on unequal lengths. Tag that cell `raises-exception`.
- `23-concurrency/01-threads-lesson`: add one sentence after the GIL line: "Since 3.14 there is also an officially supported free-threaded build (`python3.14t`) without the GIL. The default build still has it."
- Make the challenge reference `threeSum` and `merge` sort a copy (`sorted(...)`), not the input.

1.10 **Regenerate outputs** for every lesson: `uv run python tools/refresh_outputs.py`. That script is added in Phase 2. If Phase 2 isn't done yet, add `tools/refresh_outputs.py` from Appendix E first.

**Acceptance:** Phase 2's test suite, once added, reports no failures caused by items 1.1–1.8.

---

## Phase 2: Verification harness and CI

**Goal:** the defects found in this review can't come back.

2.1 **Reference solutions.** For every practice notebook, create `solutions/<same folder>/<name without -practice>.py` containing only the solved functions and classes, with the same names as the stubs. Examples:
- `course/07-comprehensions/01-comprehensions-practice.ipynb` → `solutions/course/07-comprehensions/01-comprehensions.py`
- `challenges/problems/04-3sum.ipynb` → `solutions/challenges/problems/04-3sum.py`

For pattern and challenge solutions, add a docstring with **Approach**, **Time**, **Space**, and one **Alternative**. Exercises that aren't function-shaped may ship a fully solved notebook copy at `solutions/<folder>/<name>.ipynb` instead.

2.2 **Tests.** Add the following, all verified working against this repo during the review:
- `tests/test_practice.py` (Appendix C). Every practice notebook passes with its solution spliced in, and fails *cleanly* as shipped.
- `tests/test_lessons.py` (Appendix D). Every lesson runs in a real kernel, and its saved stdout matches a fresh run. Tag machine-dependent cells `volatile` (for example, `cpu_count()` in the processes lesson).
- `tests/test_links.py` (Appendix F2).
- `tools/refresh_outputs.py` (Appendix E).

When the harness first runs on the unfixed repo, it fails exactly on #1, #2, #3 and the stale `02-main` output.

2.3 **Practice stubs and checks:**
- Replace every `...` stub body with `raise NotImplementedError`.
- Replace bare `assert f(x) == y` lines with `check(f, x, expect=y)`, and add `from pylearn import check` in the first code cell.
- Keep plain `assert … , "message"` for stateful checks (classes, mutation checks such as "nums unchanged"). Always include a message there.
- This fixes the `TypeError`/`AttributeError` failures in the unsolved notebooks (#14).

Before:
```python
def kind(value):
    ...


assert kind(3) == "int"
```
After:
```python
from pylearn import check


def kind(value) -> str:
    raise NotImplementedError


check(kind, 3, expect="int")
check(kind, None, expect="NoneType")
```

2.4 **Lint.** `uv run ruff check .` must pass. With Appendix A's config, the current repo has 11 findings besides the camelCase names.
- Where a lesson shows a mistake on purpose (booleans lesson `False == None`, `True and False`, `False or 5`; the guide's mutable default and `[] is []`), add `# noqa: <code>` on that line. That keeps the demo and documents the intent.
- Fix the rest: import order (`ruff check --fix`), `zip(strict=True)`, and the long line in the guide.
- Rename the challenge functions to snake_case and keep the LeetCode title in the heading, e.g. `# 01. Two Sum (LeetCode 1)`. Remove the `N802` exemption once that's done.

2.5 **CI.** Add `.github/workflows/ci.yml` (Appendix F1).

**Acceptance**
- `uv run pytest -n auto` passes.
- `uv run ruff check .` passes.
- CI is green on 3.12 and 3.14. 3.15 is allowed to fail until `pyzmq` and `ipykernel` wheels exist for it.

---

## Phase 3: Lesson and practice templates

> Lesson cell order is now in `AGENTS.md` ("Lesson flow"). Use that, not the Predict-first table below.

**Goal:** lessons teach (PRIMM, worked examples with subgoal labels, error reading), and practice ramps up (Parsons warm-up, then the core task, then a stretch), with hints and reflection. Apply this one folder per commit, starting with `course/01-basics`.

### Lesson template (every `*-lesson.ipynb`)

| Cell | Type | Content |
|---|---|---|
| 1 | md | `# NN. Title`. **Tier:** Core, Intermediate, or Deep. **You will be able to:** 2–3 verbs ("predict…", "write…", "choose…"). Rough time. **Uses:** Markdown links to the earlier lessons it builds on, or `nothing yet`. |
| 2 | md | `## The idea`: 3–6 sentences giving the mental model, with no code. Then a `<details><summary>Explain more</summary>` block for beginners covering vocabulary, syntax details, and an analogy. |
| 3–4 | md + code | `## Predict`: "Write down what each line prints before you run it." Then a short code cell of 4–6 prints that probe the idea and one likely misconception. |
| 5 | md | `<details><summary>Check your predictions</summary>` explaining each surprising line. |
| 6–7 | md + code | `## Worked example`: a complete realistic function with **subgoal-label comments** (`# 1. Handle the missing value first.`). It solves a *different* problem from the practice, from start to end. A pattern lesson solves a sibling that is not in `challenges/problems/`. |
| 8 | md | `## Why it works this way`: the mechanism underneath, what it costs in time and memory, and the design reason. Link the matching `internals/` lesson. Do not restate the fact. |
| 9 | md | `## When to use it`: when this is the right tool, when it isn't, and what to use instead. |
| 10–11 | md + code | `## Common mistake`: the bug learners actually make. If it raises, tag `raises-exception` and say how to read the traceback: last line first, then the arrowed line. If it is silent, print the wrong result, then show the fix in the next cell and say why it was wrong. Not a one-liner whose only point is that an error exists. |
| 12 | md | `## Investigate`: 2–3 questions about the worked example, with answers in `<details>`. |
| 13 | md | `## Modify`: one small change to make to the worked example, and the question it raises. |
| 14 | md | `## Recap`: three bullets, then `Next: [practice](NN-name-practice.ipynb)`. |

Word targets, excluding code: Core 350–600, Intermediate 600–1,000, Deep 900–1,600 with a diagram or trace table. Tag the tier in the first cell. Don't pad. Split a lesson that needs more than its tier.

### Practice template (every `*-practice.ipynb`)

| Cell | Type | Content |
|---|---|---|
| 1 | md | Title. "Replace `raise NotImplementedError`, run the cell, and read the ✓ lines or the error. Open hints in order only when stuck." One-line link back to the lesson. |
| 2 | code | `from pylearn import check` (plus any imports the exercises need). |
| 3–4 | md + code | `## Warm-up`: a **Parsons problem** (the solution's lines scrambled in a comment, which you reorder and indent) or a fill-in-the-blank. |
| 5–6 | md + code | `## Core`: the main task with 4–6 `check` calls, including edge cases. Two or three `<details>` hints that go from concept to approach to near-code. |
| 7–8 | md + code | `## Stretch` (optional): a twist that needs the same idea. |
| 9 | md | `## Reflect`: one question to answer in a sentence, e.g. "Why must the `None` check come first?" |

### Worked example: `course/01-basics/03-booleans` → `03-conditions`

This shows the full standard. It also fixes #7 by teaching `if` right where booleans are introduced.

**Lesson cells**

````markdown
# 03. Conditions: True, False, None, and `if`

**You will be able to:** predict the result of a comparison and of `and` / `or`; choose a branch with `if` / `elif` / `else`; test for a missing value with `is None`.
About 20 minutes. **Uses:** 01 Names, 02 Numbers.
````

````markdown
## The idea

A comparison such as `n < 0` produces a value: `True` or `False`. `if` runs its indented block only when its condition is true. `elif` is checked only when every branch above it was false, and `else` catches whatever is left. `None` means "no value yet". It isn't `False` and it isn't `0`, so ask about it directly with `value is None`.

<details><summary>Explain more</summary>

The colon at the end of `if n < 0:` starts a block. The block is the lines indented under it (4 spaces). `=` stores a value; `==` compares two values. `is` asks whether two names point at the very same object, which is how you test for `None`.
</details>
````

```python
print(3 < 5)
print(0 == False)
print(None == False)
print(None is None)
print(True and False)
print(0 or "default")
```

````markdown
<details><summary>Check your predictions</summary>

- `0 == False` is `True`: a bool is a kind of int, and `False` equals 0.
- `None == False` is `False`: `None` is its own value.
- `0 or "default"` prints `default`: `or` returns the first operand that counts as true, not the word `True`.
</details>
````

```python
def describe(n: int | None) -> str:
    # 1. Handle the missing value first.
    if n is None:
        return "missing"
    # 2. Check special cases, most specific first.
    if n < 0:
        return "negative"
    # 3. Everything else.
    return "ok"


print(describe(None), describe(-1), describe(0), describe(2))
```

Common mistake. This one raises, so tag the cell `raises-exception`. The Markdown above it reads: "The last line of the error names the problem: Python can't compare `None` with a number. Check for `None` first." A silent mistake instead prints the wrong result, then the next cell shows the fix and says why.

```python
def describe_wrong(n):
    if n < 0:
        return "negative"
    if n is None:
        return "missing"
    return "ok"


describe_wrong(None)
```

- **Investigate:** (1) Why does `describe(0)` return `"ok"` and not `"missing"`? (2) What would `if not n:` do differently from `if n is None:`? Try it.
- **Modify:** make `0` return `"zero"`. Where must the new branch go, and why?

**Practice cells** (`03-conditions-practice.ipynb`; the solution goes in `solutions/course/01-basics/03-conditions.py`)

```python
from pylearn import check
```

```python
# Warm-up: these lines of `sign` are scrambled. Rebuild the function with correct indentation.
#     return "zero"
# if n > 0:
#     return "positive"
# return "negative"
# if n == 0:


def sign(n: int) -> str:
    raise NotImplementedError


check(sign, 5, expect="positive")
check(sign, 0, expect="zero")
check(sign, -3, expect="negative")
```

```python
# Core: None is "missing". 90 and above is "A", 80 to 89 is "B", anything lower is "C".
def grade(score: int | None) -> str:
    raise NotImplementedError


check(grade, None, expect="missing")
check(grade, 95, expect="A")
check(grade, 90, expect="A")
check(grade, 89, expect="B")
check(grade, 0, expect="C")
```

```python
# Stretch: return the first argument that is not None. 0 and "" count as present.
def first_present(a, b, c):
    raise NotImplementedError


check(first_present, None, 0, 5, expect=0)
check(first_present, None, None, "", expect="")
check(first_present, None, None, None, expect=None)
```

Reflect: "In one sentence: why does `a or b or c` give the wrong answer for `first_present`?"

**Acceptance (per folder):** every lesson and practice in the folder matches the templates, `uv run pytest` passes, and outputs have been regenerated.

---

## Phase 4: One language course and the missing topics

**Goal:** one numbered sequence for the language, with the topic gaps filled. Part 2 is about writing real programs in `.py` files with pytest.

4.1 **Moves** (`git mv`, then fix links):

| From | To |
|---|---|
| `course/11-hash-maps` … `course/20-design` | `patterns/` (see Phase 5 for numbering) |
| `course/10-classes/02-linked-lists-*` | `patterns/07-linked-lists/01-traversal-*` |
| `course/21-modules` | `course/12-modules` |
| `course/22-files` | `course/13-files` |
| `course/24-testing` | `course/14-testing` |
| `course/23-concurrency` | `course/16-concurrency` |

4.2 **Target sequence.** "new" marks lessons to write. Each one is a lesson plus practice, following the Phase 3 templates.

**Part 1: The language** (notebooks)
- `00-start`
  - 01 First program, new: a `hello.py` run with `uv run python hello.py`; `print`, `input`, comments; reading your first error.
  - 02 How practice works, new: `def`, `return`, calling a function, `check`. Type hints in two sentences: "labels for readers and tools; Python doesn't enforce them."
- `01-basics`: names, numbers, conditions (Phase 3 example).
- `02-strings`: indexing, methods, formatting. Add format specs (`:.2f`, `:>8`, `:,`).
- `03-collections`: lists, tuples (with unpacking), dicts, sets.
- `04-control-flow`: `match`, loops, `enumerate` and `zip(strict=True)`.
- `05-functions`: definitions, arguments (keyword-only, defaults), 03 scope and closures (new), 04 docstrings and type hints (new).
- `06-errors`: try/except/else/finally, 02 `raise` and custom exceptions (new), 03 reading tracebacks and `breakpoint()` (new).
- `07-iteration`: comprehensions (list, dict, set, generator expressions), 02 iterators and generators (new), 03 sorting with `key=` and `lambda` (new).
- `08-collections-module`: Counter, defaultdict, deque, heapq, 05 itertools and `functools.cache` (new).
- `09-pitfalls`: mutable defaults, shared rows, identity, 04 late-binding closures (new), 05 float precision and `Decimal` (new).
- `10-classes`: classes (add `__repr__`, `__eq__`), 02 dataclasses (new), 03 inheritance and `super()` (new), 04 properties, `classmethod`, `staticmethod` (new), 05 enums (new).
- `11-data-model`, new: dunder methods (`__len__`, `__iter__`, `__getitem__`, `__contains__`), 02 context managers (`with`, writing one).

**Part 2: Writing real programs** (each unit = a short lesson notebook plus an `exercise/` folder with `.py` stubs and `test_*.py`, run by `uv run pytest course/NN-*/exercise`)
- `12-modules`: imports, `__main__` (Phase 1 version), packages, `uv add`, and virtual environments explained.
- `13-files`: `open`/`with`/`encoding="utf-8"`, `Path.read_text`/`write_text`, csv, json. Exercise: read a CSV, write a JSON summary, tested with `tmp_path`.
- `14-testing`: **pytest first** (asserts, `parametrize`, fixtures, `tmp_path`, `raises`); unittest as a short "you'll see this in older code" note. Exercise: write tests that catch three planted bugs in a given module.
- `15-decorators`, new: functions as values, writing a decorator, `functools.wraps`.
- `16-concurrency`: threads, processes (the exercise is a script using `ProcessPoolExecutor` under a `__main__` guard), asyncio (Phase 1 version), a free-threading note.
- `17-tooling`, new: ruff, a type checker (mypy or pyright; mention Astral's `ty` as beta), `logging` instead of `print`.

4.3 **Concept ledger.** Create `docs/concepts.md`, a table of concept id → lesson that introduces it. Then add `tools/check_sequence.py` and `tests/test_sequence.py`. They walk `course/` in order, parse each code cell with `ast` (skip cells that start with `%` or `!`), map node types to concept ids, and fail when a notebook uses a concept introduced later. Mapping:

| AST node | Concept id |
|---|---|
| `If`, `IfExp` | `conditions` |
| `For`, `While` | `loops` |
| `FunctionDef`, `Return` | `functions-basic` (allowed from `00-start/02`) |
| `ClassDef` | `classes` |
| `ListComp`, `DictComp`, `SetComp`, `GeneratorExp` | `comprehensions` |
| `Try` | `exceptions` |
| `Raise` | `raise` (except `raise NotImplementedError` in stubs) |
| `With` | `with` |
| `Lambda` | `lambda` |
| `Match` | `match` |
| `Yield` | `generators` |
| `AsyncFunctionDef`, `Await` | `async` |
| decorators on a def | `decorators` |
| `JoinedStr` | `f-strings` |
| `Starred` in a call or signature | `star-args` |

4.4 **Exercise loading.** Part 2 tests use `pylearn.load_exercise("name")`, which loads `name.py` from the test's folder. CI sets `PYLEARN_SOLUTIONS=1` to load `solutions/<same folder>/name.py` instead. Add this CI step now (Appendix F1 has it commented out).

**Acceptance:** `uv run pytest -n auto` passes, `PYLEARN_SOLUTIONS=1 uv run pytest course` passes, and `docs/language.md` and `docs/start-here.md` reflect the new sequence.

---

## Phase 5: Patterns and challenges section

**Goal:** pattern lessons teach on *sibling* problems, so the challenge problems stay unseen. Add the missing pattern families, test properly, and practise the newer challenge formats.

5.1 **`patterns/` layout.** Each unit has a lesson on the "Lesson" problem below and a practice on the "Pattern practice" problem. The "Challenge" problems live only in `challenges/problems/`, and the pattern unit must not solve them.

| # | Pattern | Lesson (worked) | Pattern practice | Challenge problems (unseen) |
|---|---|---|---|---|
| 01 | Hash maps & sets | Contains Duplicate | Valid Anagram; First Unique Character | Two Sum, Group Anagrams, Top K Frequent |
| 02 | Two pointers | Valid Palindrome | Two Sum II (sorted pair; existing) | 3Sum, Container With Most Water, Trapping Rain Water |
| 03 | Sliding window | Max sum of a k-window (existing) | Minimum Size Subarray Sum | Longest Substring Without Repeating, Minimum Window Substring |
| 04 | Prefix sums & running state | Running Sum; Range Sum Query | Find Pivot Index | Best Time to Buy/Sell Stock, Product Except Self, Maximum Subarray |
| 05 | Binary search | Search Insert Position (`bisect`) | First Bad Version | Binary Search, Search in Rotated, Find Min in Rotated |
| 06 | Stacks & monotonic stack | Backspace String Compare; Next Greater Element | Min Stack | Valid Parentheses, Daily Temperatures |
| 07 | Linked lists | Traversal & dummy head (moved from classes) | Middle of the Linked List (fast/slow) | Reverse List, Merge Two Lists, Linked List Cycle, Merge K Lists |
| 08 | Intervals | Meeting overlap check | Meeting Rooms (can attend all?) | Merge Intervals, Insert Interval |
| 09 | Heaps | k smallest (existing course lesson) | Last Stone Weight | Kth Largest, Find Median from Data Stream |
| 10 | Trees (new) | Traversals: pre/in/post order, level order | Same Tree | Max Depth, Invert Tree, Validate BST, Level Order, LCA of BST |
| 11 | Graphs | Flood Fill (grid DFS/BFS) | Find if Path Exists in Graph | Number of Islands, Rotting Oranges, Course Schedule (topological sort) |
| 12 | Backtracking (new) | Subsets | Letter Case Permutation | Combination Sum, Generate Parentheses, Word Search |
| 13 | Dynamic programming | Fibonacci: memo → table → two variables | Min Cost Climbing Stairs | Climbing Stairs, House Robber, Coin Change, Unique Paths, Longest Common Subsequence |
| 14 | Tries (new) | Insert/search by hand | Longest Common Prefix | Implement Trie |
| 15 | Design | OrderedDict and a doubly linked list | Design HashSet | LRU Cache |

5.2 **Challenge problem template** (every `challenges/problems/NN-*.ipynb`):
- **Heading:** `# NN. Title (LeetCode N)`, then the statement, **Constraints** (input sizes and value ranges), and **Target** (the time/space you should reach).
- **Before you code** (Markdown): restate, ask about edge cases, state the brute force and its cost.
- **Hints:** three collapsed `<details>` hints: pattern name, then key insight, then near-code.
- **Stub and checks**, in four parts: (1) examples, (2) edge cases, (3) randomized cross-check against a definition or brute force, (4) a scale check at the constraint size. The scale check should fail an O(n²) solution in seconds, not minutes.
- **After you pass** (Markdown): "State time and space. Name one edge case the checks miss. What changes if the input streams in?"

Example checks cell for Top K Frequent (verified: an O(n) Counter solution passes in ~20 ms; a `nums.count` quadratic solution fails the scale check):

```python
import random
import time
from collections import Counter


def is_valid_top_k(nums: list[int], k: int, got: list[int]) -> bool:
    """True when got holds k distinct values whose counts are the k largest counts."""
    counts = Counter(nums)
    best = sorted(counts.values(), reverse=True)[:k]
    return len(set(got)) == k and sorted((counts[v] for v in got), reverse=True) == best


# 1. Examples
assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert top_k_frequent([1], 1) == [1]
# 2. Edge cases: negatives; k equals the number of distinct values
assert sorted(top_k_frequent([-1, -1, 2], 2)) == [-1, 2]
# 3. Random inputs, checked against the definition (ties allowed)
rng = random.Random(0)
for _ in range(300):
    nums = [rng.randint(-5, 5) for _ in range(rng.randint(1, 30))]
    k = rng.randint(1, len(set(nums)))
    got = top_k_frequent(list(nums), k)
    assert is_valid_top_k(nums, k, got), f"nums={nums}, k={k}, got={got}"
# 4. Scale: n = 100,000 should take well under a second
big = [rng.randint(0, 5_000) for _ in range(100_000)]
start = time.perf_counter()
top_k_frequent(big, 10)
elapsed = time.perf_counter() - start
assert elapsed < 1.0, f"{elapsed:.2f}s for n=100,000; look for a quadratic step"
print(f"all checks passed ({elapsed * 1000:.0f} ms at n=100,000)")
```

5.3 **Solutions.** Move the five reference solutions out of `challenges/guide.ipynb` into `solutions/challenges/problems/`. Write the rest, each with Approach / Time / Space / Alternative / Common bugs. The guide links to the folder and says when to open it.

5.4 **Codebase rounds (new).** Add `challenges/codebase-rounds/01-library-checkout/`:
- A 4–5 module package (`models.py`, `store.py`, `loans.py`, `report.py`) with a pytest suite.
- **Phase A:** one test fails because of a planted bug (a mutable default shared across loans).
- **Phase B:** a feature spec in the README (holds queue: first come, first served).
- **Phase C:** a scale test with 100,000 books that fails because `store.find()` is a linear scan, so the learner adds an index.
- README rules: 60-minute box; AI assistant allowed; run the tests after every AI suggestion; write one sentence per AI change saying why it's correct.
- Solution in `solutions/challenges/codebase-rounds/01-library-checkout/`.
- Add a second round later on a different domain.

5.5 **Mock protocol.** Add `docs/guides/timed-session.md`: a 45-minute script (5 restate, 5 approach, 25 code, 5 test, 5 complexity and follow-ups), a self-scoring rubric (problem solving, code quality, verification, communication), and a log table for re-attempt dates (next day, then 1 week).

5.6 Update `docs/guides/challenge-practice.md` days and links for the new problem list (~45 problems).

**Acceptance:** no challenge problem's checks or solution appear in `patterns/` (add `tests/test_no_leaks.py`, which compares function names and the bodies of `assert` lines), all solutions pass, and the codebase round's tests fail on the stub and pass on the solution.

---

## Phase 6: Use cases become projects

**Goal:** six real projects built with real libraries. The other fields stay as short "Explore" pages.

6.1 **Deep projects.** Folder: `use-cases/<NN>-<name>/project/`. Each has its own dependency group in `pyproject.toml`.

| Project | Builds | Libraries (dependency group) |
|---|---|---|
| Automation: `tidy` | Sort a downloads folder by type and date; `--dry-run`; an undo log | stdlib, `typer` (`automation`) |
| Data analysis: `expenses` | Clean sample bank CSVs, categorize with rules, monthly summary, one chart, a narrative notebook | `polars` or `pandas`, `matplotlib` (`data`) |
| Web API: `notes-api` | CRUD notes API with validation and a SQLite store | `fastapi`, `pydantic`, `httpx` for tests (`web`) |
| AI app: `ticket-triage` | Classify support tickets with an LLM into a pydantic schema; a 30-ticket labeled eval set; accuracy report; retries and timeouts | provider SDK behind a small `Client` protocol; **`FakeClient` for offline tests**; key from env var (`ai`) |
| CLI & packaging: `csvtool` | Subcommands, an entry point, `uv build`, `uv tool install .` | `typer`, `rich` (`cli`) |
| HTTP client: `price-watch` | Fetch and parse pages from **saved HTML fixtures** in tests; rate limit; cache; store history in SQLite | `httpx`, `selectolax` or `beautifulsoup4` (`scrape`) |

6.2 **Each project has:**
- `README.md`: goal, user story, 3–4 milestones (each with acceptance tests), stretch goals, and "what you'll practise".
- `src/<pkg>/` stubs and `tests/` covering every milestone.
- `solutions/use-cases/<NN>/project/`.
- Tests that pass offline. Network and real API calls are opt-in behind an env var.

6.3 **Explore pages.** Rename the remaining fields' section in `use-cases/README.md` to "Explore". Keep their pages short, and change step 2 of "Do this first" into a task that differs from the lesson snippet.

6.4 **Order.** Put the AI app right after Web API, since it reuses pydantic and HTTP ideas.

**Acceptance:** `PYLEARN_SOLUTIONS=1 uv run pytest use-cases` passes, and each project's `uv sync --group <name>` works on a clean clone.

---

## Phase 7: Audience paths and guardrails

7.1 **Paths.** Add `docs/paths/`:
- `beginner.md`: Part 1 with "Explain more" blocks open; 30–45 minutes a day; when to ask for help; how to use the practice-tutor rule.
- `experienced.md`: take the skip test, skim Part 1 "The idea" cells, then do Part 2 fully; plus an "if you know Java / JavaScript / C#" table of 15 differences (truthiness, integer division, mutability and aliasing, scoping, EAFP, iteration protocol, duck typing, GIL, packaging).
- `challenge-practice.md`: weeks 1–2 patterns, weeks 3–4 problems with spaced re-attempts, week 5 mocks and a codebase round.
- `builder.md`: minimum of Part 1, then one project end to end.
- `instructor.md`: objectives and timings per unit, where `solutions/` is, common misconceptions per unit, suggested pair-programming format.

7.2 **Skip test.** Add `course/00-start/00-skip-test.ipynb`: 15 short questions, each mapped to a unit. A score table at the end says which units to skip.

7.3 **AI guardrail check.** Walk through `docs/ai.md` once per tool and confirm each guardrail works:
- **Cursor:** ask the agent to "solve this" on a practice notebook. It should give a hint.
- **Claude Code:** under the learner profile, a request to edit a practice notebook is denied, and reading `solutions/` is denied.
- **Claude app:** a Project with the pasted instructions answers with a hint.

Record the results in `docs/ai.md`.

**Acceptance:** each path links only to things that exist (`tests/test_links.py`), and the skip-test notebook passes in `tests/test_lessons.py`.

---

## Appendix A: `pyproject.toml`

```toml
[project]
name = "learn-python"
version = "0.1.0"
description = "Lessons, practice, timed challenges, and projects for learning Python."
readme = "README.md"
license = "MIT"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "ipykernel>=6.29",
    "nbclient>=0.10",
    "nbformat>=5.10",
    "pytest>=8",
    "pytest-xdist>=3",
    "ruff>=0.12",
]

[build-system]
requires = ["hatchling>=1.27"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/pylearn"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
target-version = "py312"
line-length = 100
extend-exclude = ["review"]

[tool.ruff.lint]
select = ["E", "F", "W", "B", "UP", "N", "SIM", "I"]

[tool.ruff.lint.per-file-ignores]
"course/**/*-practice.ipynb" = ["F401"]        # imports in practice are hints
"course/*pitfalls*/*.ipynb" = ["B006", "F632"]  # the mistake is the lesson
"challenges/**/*.ipynb" = ["N802"]               # remove after the snake_case rename
```

## Appendix B: `src/pylearn/__init__.py` and `src/pylearn/check.py`

```python
"""Helpers for the learn-python notebooks and exercises."""

from pylearn.check import check, load_exercise

__all__ = ["check", "load_exercise"]
```

```python
"""Friendly checks for practice notebooks and exercise tests."""

from __future__ import annotations

import importlib.util
import inspect
import math
import os
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

NOT_WRITTEN = "not written yet. Replace `raise NotImplementedError` with your code."


def check(func: Callable[..., Any], *args: Any, expect: Any, tol: float | None = None) -> None:
    """Call ``func(*args)`` and compare the result with ``expect``.

    Prints one line when it matches. Raises AssertionError that names the call,
    the result, and the expected value when it does not. Pass ``tol`` to compare
    floats with a tolerance.
    """
    call = f"{func.__name__}({', '.join(repr(arg) for arg in args)})"
    try:
        got = func(*args)
    except NotImplementedError:
        raise AssertionError(f"{call} is {NOT_WRITTEN}") from None
    same = math.isclose(got, expect, abs_tol=tol) if tol is not None else got == expect
    if not same:
        raise AssertionError(f"{call} returned {got!r}; expected {expect!r}")
    print(f"✓ {call} == {expect!r}")


def _repo_root(start: Path) -> Path:
    for folder in (start, *start.parents):
        if (folder / "pyproject.toml").exists():
            return folder
    raise FileNotFoundError(f"no pyproject.toml above {start}")


def load_exercise(name: str) -> ModuleType:
    """Load ``<name>.py`` from the folder of the test file that calls this.

    With the environment variable PYLEARN_SOLUTIONS=1 (CI sets it), load the
    reference solution from the same relative path under ``solutions/``.
    """
    folder = Path(inspect.stack()[1].filename).resolve().parent
    if os.environ.get("PYLEARN_SOLUTIONS") == "1":
        root = _repo_root(folder)
        folder = root / "solutions" / folder.relative_to(root)
    path = folder / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"exercise_{name}_{abs(hash(folder))}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

Example Part 2 test (`course/14-testing/exercise/test_textstats.py`):

```python
import pytest

from pylearn import load_exercise

textstats = load_exercise("textstats")


@pytest.mark.parametrize(("text", "expected"), [("", 0), ("one", 1), ("  two  words ", 2)])
def test_word_count(text, expected):
    assert textstats.word_count(text) == expected
```

## Appendix C: `tests/test_practice.py`

```python
"""Every practice notebook must pass with its reference solution, and must fail
cleanly (NotImplementedError or AssertionError) as shipped.

The reference solution is solutions/<same folder>/<name>.py. Its top-level
functions and classes replace the same-named stubs in the notebook. An exercise
that is not function-shaped can instead ship a fully solved copy at
solutions/<same folder>/<name>.ipynb, which runs as-is.
"""

from __future__ import annotations

import ast
import pathlib

import nbformat
import pytest
from nbclient import NotebookClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = (
    "course/*/*-practice.ipynb",
    "patterns/*/*-practice.ipynb",
    "challenges/problems/*.ipynb",
)
PRACTICE = sorted(p for pattern in PATTERNS for p in ROOT.glob(pattern))
CLEAN_FAILURES = {"NotImplementedError", "AssertionError"}
DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def solution_for(notebook: pathlib.Path) -> pathlib.Path:
    rel = notebook.relative_to(ROOT)
    stem = rel.name.removesuffix(".ipynb").removesuffix("-practice")
    return ROOT / "solutions" / rel.parent / f"{stem}.py"


def top_level_defs(source: str) -> dict[str, str]:
    tree = ast.parse(source)
    return {n.name: ast.get_source_segment(source, n) for n in tree.body if isinstance(n, DEFS)}


def splice(cell_source: str, solution: dict[str, str]) -> str:
    """Replace each top-level def/class that the solution also defines."""
    tree = ast.parse(cell_source)
    lines = cell_source.splitlines(keepends=True)
    targets = [n for n in tree.body if isinstance(n, DEFS) and n.name in solution]
    for node in sorted(targets, key=lambda n: n.lineno, reverse=True):
        start = (node.decorator_list[0].lineno if node.decorator_list else node.lineno) - 1
        lines[start : node.end_lineno] = [solution[node.name] + "\n"]
    return "".join(lines)


def first_error(nb: nbformat.NotebookNode, path: pathlib.Path) -> str | None:
    client = NotebookClient(
        nb,
        timeout=60,
        kernel_name="python3",
        allow_errors=True,
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()
    for cell in nb.cells:
        for out in cell.get("outputs", []):
            if out.output_type == "error":
                return f"{out.ename}: {out.evalue}"
    return None


def ids(p: pathlib.Path) -> str:
    return str(p.relative_to(ROOT))


@pytest.mark.parametrize("path", PRACTICE, ids=ids)
def test_reference_solution_passes(path: pathlib.Path) -> None:
    sol = solution_for(path)
    solved_notebook = sol.with_suffix(".ipynb")
    if solved_notebook.exists():  # for exercises that are not function-shaped
        assert first_error(nbformat.read(solved_notebook, as_version=4), path) is None
        return
    assert sol.exists(), f"missing reference solution: {sol.relative_to(ROOT)}"
    solution = top_level_defs(sol.read_text(encoding="utf-8"))
    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = splice(cell.source, solution)
    assert first_error(nb, path) is None


@pytest.mark.parametrize("path", PRACTICE, ids=ids)
def test_unsolved_notebook_fails_cleanly(path: pathlib.Path) -> None:
    nb = nbformat.read(path, as_version=4)
    error = first_error(nb, path)
    assert error is not None, "the unsolved notebook passes; the checks test nothing"
    assert error.split(":")[0] in CLEAN_FAILURES, f"confusing failure for a learner: {error}"
```

## Appendix D: `tests/test_lessons.py`

```python
"""Every lesson notebook must run top to bottom in a real kernel, and its saved
output must match what a fresh run prints.

Tag a cell `raises-exception` when the error is the lesson. Tag a cell
`volatile` when its output differs by machine (CPU count, timings, paths).
"""

from __future__ import annotations

import pathlib

import nbformat
import pytest
from nbclient import NotebookClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = (
    "course/*/*-lesson.ipynb",
    "patterns/*/*-lesson.ipynb",
    "use-cases/*/*.ipynb",
    "challenges/*.ipynb",
)
LESSONS = sorted(p for pattern in PATTERNS for p in ROOT.glob(pattern))


def stdout(cell: nbformat.NotebookNode) -> str:
    return "".join(
        out.get("text", "")
        for out in cell.get("outputs", [])
        if out.get("output_type") == "stream" and out.get("name") == "stdout"
    )


@pytest.mark.parametrize("path", LESSONS, ids=lambda p: str(p.relative_to(ROOT)))
def test_lesson_runs_and_outputs_are_fresh(path: pathlib.Path) -> None:
    saved = nbformat.read(path, as_version=4)
    fresh = nbformat.read(path, as_version=4)
    NotebookClient(
        fresh,
        timeout=60,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    ).execute()
    for old, new in zip(saved.cells, fresh.cells, strict=True):
        if new.cell_type != "code" or "volatile" in new.metadata.get("tags", []):
            continue
        assert stdout(old) == stdout(new), (
            f"saved output is stale in cell {new.get('id')}; "
            "run `uv run python tools/refresh_outputs.py` and commit"
        )
```

## Appendix E: `tools/refresh_outputs.py`

```python
"""Re-run lesson notebooks in place and clear outputs from practice notebooks.

Usage:
    uv run python tools/refresh_outputs.py            # every notebook
    uv run python tools/refresh_outputs.py PATH ...   # just these
"""

from __future__ import annotations

import pathlib
import sys

import nbformat
from nbclient import NotebookClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP = {".venv", ".ipynb_checkpoints", "solutions", "review"}


def is_practice(path: pathlib.Path) -> bool:
    return path.name.endswith("-practice.ipynb") or "problems" in path.parts


def notebooks(args: list[str]) -> list[pathlib.Path]:
    if args:
        return [pathlib.Path(arg).resolve() for arg in args]
    found = ROOT.rglob("*.ipynb")
    return sorted(p for p in found if not SKIP & set(p.relative_to(ROOT).parts))


def main(args: list[str]) -> None:
    for path in notebooks(args):
        nb = nbformat.read(path, as_version=4)
        if is_practice(path):
            for cell in nb.cells:
                if cell.cell_type == "code":
                    cell.outputs = []
                    cell.execution_count = None
        else:
            NotebookClient(
                nb,
                timeout=60,
                kernel_name="python3",
                resources={"metadata": {"path": str(path.parent)}},
            ).execute()
        nbformat.write(nb, path)
        print("updated", path.relative_to(ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
```

## Appendix F1: `.github/workflows/ci.yml`

```yaml
name: ci
on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    continue-on-error: ${{ matrix.experimental }}
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.14"]
        experimental: [false]
        include:
          - python-version: "3.15"
            experimental: true
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with:
          python-version: ${{ matrix.python-version }}
      - run: uv sync --locked
      - run: uv run ruff check .
      - run: uv run pytest -n auto
      # Phase 4+: Part 2 exercises and use-case projects, run against the reference solutions
      # - run: PYLEARN_SOLUTIONS=1 uv run pytest -n auto course use-cases
```

Bump the action major versions to the latest when you add this.

## Appendix F2: `tests/test_links.py`

```python
"""Relative links in Markdown files and notebook Markdown cells must resolve."""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKIP = {".venv", ".ipynb_checkpoints", "review", ".git"}


def documents():
    for path in sorted([*ROOT.rglob("*.md"), *ROOT.rglob("*.ipynb")]):
        if SKIP & set(path.relative_to(ROOT).parts):
            continue
        if path.suffix == ".md":
            yield path, path.read_text(encoding="utf-8")
        else:
            cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
            for cell in cells:
                if cell["cell_type"] == "markdown":
                    yield path, "".join(cell["source"])


def test_relative_links_resolve() -> None:
    broken = []
    for path, text in documents():
        for href in LINK.findall(text):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (path.parent / href.split("#")[0]).resolve()
            if not target.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {href}")
    assert not broken, "broken links:\n" + "\n".join(broken)
```

## Appendix G: Authoring instructions (`AGENTS.md` and `CLAUDE.md`)

`AGENTS.md`, read by Cursor and by Claude Code (directly, or through the `CLAUDE.md` import):

```markdown
# learn-python: instructions for coding agents

This repo teaches Python. In most sessions you are authoring course content.
If the user is a learner asking for help with an exercise, follow
docs/ai/tutor-prompt.md instead, and don't edit their exercise files.

## Layout
- course/: the language course. NN-topic/NN-name-lesson.ipynb plus NN-name-practice.ipynb. Part 2 units add an exercise/ folder (.py stubs plus test_*.py).
- patterns/: algorithm patterns, each taught on a sibling problem, not the challenge problem.
- challenges/: guide.ipynb, problems/, codebase-rounds/.
- use-cases/: projects and explore pages.
- solutions/: reference solutions at the mirrored path. Never link to them from learner files.
- src/pylearn/: check() and load_exercise().
- tests/ and tools/: the harness. review/ is read-only notes.

## Commands
- Setup: uv sync
- All checks: uv run pytest -n auto && uv run ruff check .
- Part 2 and projects against solutions: PYLEARN_SOLUTIONS=1 uv run pytest course use-cases
- Refresh notebook outputs: uv run python tools/refresh_outputs.py <paths>

## Authoring standards
- Follow the lesson and practice templates in review/AGENT_PLAN.md (Phase 3).
- Never type notebook outputs. Execute with tools/refresh_outputs.py.
- Every practice exercise has a reference solution under solutions/ at the mirrored path. Run the checks before finishing.
- Practice stubs use `raise NotImplementedError`. Checks use `pylearn.check`, or `assert ..., "message"`.
- Never put a solution in a learner-facing file. Hints go in collapsed <details> blocks, ordered from concept to approach to near-code.
- Don't use a concept before the lesson that introduces it (docs/concepts.md). Rewrite the exercise instead.
- course/ and patterns/ use the standard library only.
- A notebook cell meant to error is tagged raises-exception. Machine-dependent output is tagged volatile.
- `asyncio.run` never appears in a notebook; use top-level await. Code that must run as a program goes in a .py file run with subprocess or pytest.
- Pattern lessons and practice must not solve any problem in challenges/problems/.
- Voice: short, plain, declarative sentences. Define a term the first time you use it. No Python version numbers in learner-facing text.
- Moves use git mv. Afterwards tests/test_links.py must pass.
```

`CLAUDE.md`, so every Claude Code version and setting loads the same instructions:

```markdown
@AGENTS.md

## Claude Code
- Authoring sessions start with plain `claude`. Learner sessions start with
  `claude --settings .claude/learner-settings.json`. If the "Python tutor"
  output style is active, this is a learner session: follow the tutor
  instructions and don't edit exercise files.
- Edit notebooks with the notebook edit tool or an nbformat script, never by
  rewriting the JSON by hand.
```

## Appendix H: Learner tutor (one text, four wrappers)

**H1. `docs/ai/tutor-prompt.md`** (canonical; edit only this, then copy it into the wrappers):

```markdown
# Python practice tutor

The person you're helping is learning Python with this repo's practice notebooks, exercise folders, and challenge problems. Learning comes from their own attempt, so:

- Don't write or complete the solution, and don't edit their exercise files, unless their message contains the exact phrase SHOW SOLUTION.
- Give the smallest useful hint first, then go one level deeper per follow-up: a question → the concept or pattern name → the approach in words → pseudocode for one step.
- When a check fails, point to the failing check, ask what they expected, and explain how to read the traceback: last line first, then the line marked with an arrow.
- When their code passes, ask for its time and space complexity and one edge case the checks miss. Suggest re-attempting it from memory tomorrow.
- Don't open or quote files under solutions/.
- In codebase rounds, AI help is allowed: ask them to run the tests and explain each change in one sentence before accepting it.
```

**H2. `.cursor/rules/practice-tutor.mdc`** (Apply Intelligently: no globs, so it stays out of authoring sessions):

```markdown
---
description: Tutor mode for learners. Apply when the user asks for help solving or debugging a practice notebook, exercise, or challenge problem as a learner. Do not apply when the user is authoring or editing course content, for example following review/AGENT_PLAN.md.
alwaysApply: false
---
# Python practice tutor

The person you're helping is learning Python with this repo's practice notebooks, exercise folders, and challenge problems. Learning comes from their own attempt, so:

- Don't write or complete the solution, and don't edit their exercise files, unless their message contains the exact phrase SHOW SOLUTION.
- Give the smallest useful hint first, then go one level deeper per follow-up: a question → the concept or pattern name → the approach in words → pseudocode for one step.
- When a check fails, point to the failing check, ask what they expected, and explain how to read the traceback: last line first, then the line marked with an arrow.
- When their code passes, ask for its time and space complexity and one edge case the checks miss. Suggest re-attempting it from memory tomorrow.
- Don't open or quote files under solutions/.
- In codebase rounds, AI help is allowed: ask them to run the tests and explain each change in one sentence before accepting it.
```

**H3. `.claude/output-styles/python-tutor.md`** (Claude Code custom output style):

```markdown
---
name: Python tutor
description: Hints, not answers, for this repo's practice notebooks and challenge problems
keep-coding-instructions: true
---
# Python practice tutor

The person you're helping is learning Python with this repo's practice notebooks, exercise folders, and challenge problems. Learning comes from their own attempt, so:

- Don't write or complete the solution, and don't edit their exercise files, unless their message contains the exact phrase SHOW SOLUTION.
- Give the smallest useful hint first, then go one level deeper per follow-up: a question → the concept or pattern name → the approach in words → pseudocode for one step.
- When a check fails, point to the failing check, ask what they expected, and explain how to read the traceback: last line first, then the line marked with an arrow.
- When their code passes, ask for its time and space complexity and one edge case the checks miss. Suggest re-attempting it from memory tomorrow.
- Don't open or quote files under solutions/.
- In codebase rounds, AI help is allowed: ask them to run the tests and explain each change in one sentence before accepting it.
```

**H4. `.claude/learner-settings.json`** (Claude Code learner profile; start with `claude --settings .claude/learner-settings.json`):

```json
{
  "outputStyle": "Python tutor",
  "permissions": {
    "deny": [
      "Read(**/solutions/**)",
      "Edit(**/*-practice.ipynb)",
      "Edit(**/challenges/problems/**)",
      "Edit(**/exercise/**)"
    ]
  }
}
```

Deny rules stop Claude's own file tools, which is the point. They don't stop a script Claude runs from writing files, so treat them as a guardrail, not a lock. For use-case projects, learners should drop the profile and use `/output-style learning` instead. Claude then builds the routine parts and leaves `TODO(human)` spots for the learner.

**H5. `docs/ai/claude-project-instructions.md`** (Claude app on web, desktop, or mobile, where there's no repo access):

```markdown
# Using the Claude app as your tutor

1. In Claude, create a Project called "Learn Python".
2. Paste everything below the line into the Project's instructions.
3. In each chat, choose the **Learning** style from the style menu.
4. Paste your code and the full error, or attach the notebook.

---

# Python practice tutor

The person you're helping is learning Python with this repo's practice notebooks, exercise folders, and challenge problems. Learning comes from their own attempt, so:

- Don't write or complete the solution, and don't edit their exercise files, unless their message contains the exact phrase SHOW SOLUTION.
- Give the smallest useful hint first, then go one level deeper per follow-up: a question → the concept or pattern name → the approach in words → pseudocode for one step.
- When a check fails, point to the failing check, ask what they expected, and explain how to read the traceback: last line first, then the line marked with an arrow.
- When their code passes, ask for its time and space complexity and one edge case the checks miss. Suggest re-attempting it from memory tomorrow.
- Don't open or quote files under solutions/.
- In codebase rounds, AI help is allowed: ask them to run the tests and explain each change in one sentence before accepting it.
```

**H6. `tests/test_ai_instructions.py`**:

```python
"""Every AI tool gets the same tutor instructions, word for word."""

from __future__ import annotations

import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "docs" / "ai" / "tutor-prompt.md"
WRAPPERS = (
    ".cursor/rules/practice-tutor.mdc",
    ".claude/output-styles/python-tutor.md",
    "docs/ai/claude-project-instructions.md",
)


@pytest.mark.parametrize("wrapper", WRAPPERS)
def test_wrapper_contains_canonical_tutor_text(wrapper: str) -> None:
    canonical = CANONICAL.read_text(encoding="utf-8").strip()
    text = (ROOT / wrapper).read_text(encoding="utf-8")
    assert canonical in text, f"{wrapper} drifted from docs/ai/tutor-prompt.md"


def test_learner_profile() -> None:
    settings = json.loads((ROOT / ".claude" / "learner-settings.json").read_text(encoding="utf-8"))
    assert settings["outputStyle"] == "Python tutor"
    deny = settings["permissions"]["deny"]
    assert "Read(**/solutions/**)" in deny
    assert "Edit(**/*-practice.ipynb)" in deny
```
