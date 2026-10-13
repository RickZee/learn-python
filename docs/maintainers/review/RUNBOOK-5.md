# Runbook 5: make the guards honest, then fix what they find

This runbook is for Cursor. It drives everything in [CRITIQUE-5.md](CRITIQUE-5.md) to completion. [PROGRESS-5.md](PROGRESS-5.md) is the work list and the memory between sessions. Run it after round 4 (`ROUND4-REPORT.md`).

**Start or resume with:**

> I am authoring the course. Follow `docs/maintainers/review/RUNBOOK-5.md`. Continue from the first unchecked item in `docs/maintainers/review/PROGRESS-5.md`. Do not stop until every item is checked or you hit a blocker as defined in section 2.

Start every session with the words "I am authoring the course". After item S2 lands, that sentence is what switches an agent from tutor mode to authoring mode.

---

## 1. The loop

Repeat until every box in `PROGRESS-5.md` is checked:

1. **Pick** the first unchecked item. Read its line, the section of this runbook it names, and the exemplar it names. Don't skip ahead or reorder.
2. **Do** the item in full. Full means it meets the item's *done when* and the quality bar in section 6.
3. **Verify.** Run:
   - `uv run python tools/refresh_outputs.py <changed notebooks>`
   - `uv run pytest -n 4`
   - `PYLEARN_SOLUTIONS=1 uv run pytest -n 4 course use-cases` (when you touched `course/*/exercise` or `use-cases/`)
   - `uv run ruff check .` (and `uv run ruff format --check .` after item M2)
   - `uv run python tools/depth_report.py <changed lessons>` (when you touched a lesson)

   Expected red: after S4, the new guards fail on everything listed in `docs/maintainers/status.md`. That is the work list, and those tests are `xfail(strict=True)` for exactly the listed paths. Everything else must be green. A failing test you caused is part of the item, not a reason to stop.
4. **Self-review** against section 6. Write the answers into the item's notes line in `PROGRESS-5.md`. Keep it short, for example: `57: statement 74 words; hints 3; oracle slow_edit_distance; wrong variant (no replace) caught by cross_check`.
5. **Commit** with a message naming the item, for example `R5 C03: challenge notebooks 13–24`. Tick the box in `PROGRESS-5.md` and remove the finished paths from `docs/maintainers/status.md`, both in the same commit.
6. **Go to step 1.** Don't ask for confirmation between items. Don't write summaries between items; the progress file is the summary.

**Context.** After every 3 items, make sure `PROGRESS-5.md` is committed and accurate. If the session ends, the next one resumes from the progress file. Never redo a checked item unless a later test proves it broken. If one is broken, add a `FIX:` item directly below the current one and continue.

**Branch.** Work on `review/round-5-run`, created from `main` in item S1. Merge to `main` only in item F3. Never push.

---

## 2. When you may stop

Stop and ask only for one of these. Write the blocker under **Blockers** in `PROGRESS-5.md` first.

- A package won't install, or the environment is broken in a way you can't fix inside the repo.
- Two instructions contradict each other, and choosing one would change teaching content in a way that's hard to undo.
- A test can only pass by doing something section 7 forbids.
- An item needs a decision this runbook marks **(Rick decides)**.

These are not blockers: a hard lesson, a failing test you caused, the volume of work left, uncertainty about wording (use the exemplars), or wanting a review (the notes and commits are the review).

---

## 3. Locked decisions

These override earlier rules. Item S2 copies them into `docs/maintainers/authoring.md`.

**D1. No reference implementations in learner files.**
- Random cross-checks call `pylearn.challenges.cross_check(slug, func)`. Each oracle there is slow by construction: it tries every option, uses no memo, no DP table, no clever data structure, and runs only on small inputs. It must not match the reference solution's normalized AST.
- This replaces RUNBOOK-2 §3 ("a randomized cross-check against an in-notebook brute force").
- *Property* checks stay in the notebook, because they check the output without computing the answer. Examples: Two Sum checks that the two values add to the target; Top-K checks frequencies.
- Design problems (LRU, Trie, TimeMap, MedianFinder) use random operation sequences against a slow model, for example a plain list scanned on every call. The model lives in `pylearn.challenges` too.

**D2. Challenge notebooks may link only to their own walkthrough, and only under `## After you pass`.** Remove the "Solutions:" line from every first cell. Update the solutions-link rule in AGENTS/authoring to say this.

**D3. Every assert must test something.** An assert whose test is a constant, or compares only constants, is banned everywhere. A challenge's check count counts only asserts that call the function or class under test, plus one for a `cross_check(...)` call.

**D4. A hint never contains the answer.** The last hint ("near the code") is a skeleton with `___` blanks, or at most one line of the solution. It never includes a whole function body.

**D5. Default to tutor.** `AGENTS.md` becomes a short router.
- A session is authoring only when the user says so ("I am authoring", "I'm editing the course") or points at `docs/maintainers/`, a RUNBOOK, or a PROGRESS file.
- Otherwise the agent tutors.
- Authoring rules move, unchanged in meaning, to `docs/maintainers/authoring.md`.

**D6. Hard blocks for Cursor learners are opt-in.** `uv run python tools/learner_mode.py on` writes a git-ignored `.cursorignore` and a git-ignored always-on rule. Authors never run it.

Don't commit `.cursorignore`. It would block the authoring agent from `solutions/`.

**D7. Guards normalize before they match.**
- Every banned-phrase check lowercases the text, turns `-` and `_` into spaces, and collapses whitespace before matching.
- Repetition thresholds move from "more than three notebooks" to "more than two".

**D8. Projects are milestones.**
- Each project has 4–6 milestones.
- Each milestone has its own test file, `tests/test_m<N>_<name>.py`, and its own README section.
- A learner runs `uv run pytest <project> -k m1`, then `-k m2`, and so on.

**D9. Practice has a Debug item.** The practice order is Warm-up → Core → Debug → Stretch → Reflect. Debug is a short function with the lesson's common mistake planted in it, plus checks that fail until it's fixed. Required from `course/02-strings` onward.

---

## 4. Exemplars (the quality bar; copy their shape)

### Exemplar A: a challenge notebook (`challenges/problems/57-edit-distance.ipynb`)

Cell 0 (markdown):

````markdown
# 57. Edit Distance

**Difficulty:** Hard. **Target:** O(m·n) time, O(n) extra space. **Time box:** 45 minutes.

You are given two strings, `word1` and `word2`. One *edit* is one of three moves: insert a character, delete a character, or replace one character with another. Return the smallest number of edits that turns `word1` into `word2`.

Spell checkers and `diff` tools use this number to decide how close two strings are.

**Constraints.** Each string has 0 to 500 lowercase English letters.
````

Cell 1 (markdown):

````markdown
## Examples

- `"horse"`, `"ros"` → `3`: replace `h` with `r` (`rorse`), delete `r` (`rose`), delete `e` (`ros`).
- `"intention"`, `"execution"` → `5`.
- `""`, `"abc"` → `3`: three inserts. An empty string costs the other string's length.
- `"same"`, `"same"` → `0`.
````

Cell 2 (markdown):

````markdown
## Before you code

1. If the first letters already match, do you ever need to spend an edit on them? Why not?
2. After one edit at the front, what smaller problem is left? Write it out for each of the three edits.
3. How many different pairs of suffixes can those smaller problems reach? What does that tell you about repeated work?
````

Cell 3 (markdown):

````markdown
## Hints

<details><summary>Hint 1: the pattern</summary>

This is 2D dynamic programming. Every answer is built from answers on shorter strings. Name one: `d(i, j)` is the number of edits that turn the first `i` letters of `word1` into the first `j` letters of `word2`.
</details>

<details><summary>Hint 2: the approach</summary>

If the last letters match, `d(i, j) = d(i - 1, j - 1)`. Otherwise it is one edit plus the cheapest of delete `d(i - 1, j)`, insert `d(i, j - 1)`, and replace `d(i - 1, j - 1)`. Row 0 and column 0 count up from 0, because turning a string into an empty one needs only deletes (or only inserts). Fill a table row by row so every value you read already exists.
</details>

<details><summary>Hint 3: near the code</summary>

```python
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if word1[i - 1] == word2[j - 1]:
            table[i][j] = ___
        else:
            table[i][j] = 1 + min(___, ___, ___)
```
</details>
````

Cell 4 (code):

```python
import time

from pylearn.challenges import cross_check


def min_distance(word1: str, word2: str) -> int:
    raise NotImplementedError


# 1. Examples
assert min_distance("horse", "ros") == 3
assert min_distance("intention", "execution") == 5
# 2. Edges
assert min_distance("", "") == 0
assert min_distance("", "abc") == 3
assert min_distance("abc", "") == 3
assert min_distance("same", "same") == 0
assert min_distance("ab", "ba") == 2
assert min_distance("plasma", "altruism") == 6
# 3. Random inputs against a slow version that tries every edit
cross_check("57-edit-distance", min_distance)
# 4. Scale. If this runs for more than a few seconds, interrupt it: your solution repeats work.
start = time.perf_counter()
assert min_distance("kitten" * 50, "sitting" * 50) == 150
elapsed = time.perf_counter() - start
assert elapsed < 2.0, f"{elapsed:.2f}s for 300 x 350 letters; look for repeated work"
print("all checks passed")
```

Cell 5 (markdown):

````markdown
## After you pass

1. State the time and space cost, and say why in one sentence each.
2. Shrink the table to two rows. Then to one row: which value must you save before you overwrite a cell?
3. Then read the [walkthrough](../../solutions/challenges/problems/57-edit-distance.md) and compare its trace with yours.
````

What makes it the bar:
- A real statement and constraints.
- Examples with reasons.
- Prompts about *this* problem.
- The pattern is not in the statement. Recognizing it is part of the skill, so it is Hint 1.
- Three hints, where the last one has blanks.
- A typed stub.
- Asserts that call the function.
- No oracle in the notebook.
- A scale check with a message.
- The walkthrough link comes only after the learner passes.

### Exemplar B: the `pylearn.challenges` helper

Create `src/pylearn/challenges/__init__.py` (the public API) and `src/pylearn/challenges/oracles.py` (one block per problem, in problem order). The core, already tested against the edit-distance reference solution and a wrong variant:

```python
"""Random cross-checks for challenge problems.

Each problem registers a slow reference that is correct by construction (it tries
every option) and a generator of small random inputs. A learner's function must
agree with the slow reference on every input.
"""

from __future__ import annotations

import copy
import random
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

from pylearn.check import NOT_WRITTEN


@dataclass(frozen=True)
class Oracle:
    slow: Callable[..., Any]
    cases: Callable[[random.Random], Iterator[tuple[Any, ...]]]
    same: Callable[[Any, Any], bool] = lambda got, want: got == want


ORACLES: dict[str, Oracle] = {}


def register(slug: str, oracle: Oracle) -> None:
    ORACLES[slug] = oracle


def cross_check(slug: str, func: Callable[..., Any], *, trials: int = 40, seed: int = 0) -> None:
    """Compare ``func`` with the slow reference for ``slug`` on random inputs."""
    from pylearn.challenges import oracles  # noqa: F401  (registers every problem)

    oracle = ORACLES[slug]
    rng = random.Random(seed)
    cases = oracle.cases(rng)
    for _ in range(trials):
        args = next(cases)
        want = oracle.slow(*copy.deepcopy(args))
        call = f"{func.__name__}({', '.join(repr(arg) for arg in args)})"
        try:
            got = func(*copy.deepcopy(args))
        except NotImplementedError:
            raise AssertionError(f"{call} is {NOT_WRITTEN}") from None
        if not oracle.same(got, want):
            raise AssertionError(f"{call} returned {got!r}; a slow correct version returns {want!r}")
    print(f"✓ {func.__name__} agrees with a slow reference on {trials} random inputs")
```

One oracle, in `oracles.py`:

```python
def slow_edit_distance(a: str, b: str) -> int:
    """Try all three edits at every mismatch. Exponential on purpose."""
    if not a or not b:
        return len(a) + len(b)
    if a[0] == b[0]:
        return slow_edit_distance(a[1:], b[1:])
    return 1 + min(
        slow_edit_distance(a[1:], b),  # delete
        slow_edit_distance(a, b[1:]),  # insert
        slow_edit_distance(a[1:], b[1:]),  # replace
    )


def _edit_distance_cases(rng: random.Random) -> Iterator[tuple[str, str]]:
    while True:
        yield (
            "".join(rng.choice("abc") for _ in range(rng.randint(0, 5))),
            "".join(rng.choice("abc") for _ in range(rng.randint(0, 5))),
        )


register("57-edit-distance", Oracle(slow_edit_distance, _edit_distance_cases))
```

On a mismatch, the learner sees the smallest useful failure, for example:
`min_distance('bab', 'bbbb') returned 3; a slow correct version returns 2`.
That counterexample is worth more than a bare `AssertionError`.

For design problems, add `cross_check_ops(slug, cls)`. It drives the learner's class and a slow model class with the same random operation sequence and compares every return value. Example: for 16 LRU, the model is a list of `(key, value)` pairs, scanned and reordered on every call.

Add `tests/test_challenge_oracles.py`:
- every registered slug has a notebook;
- every oracle agrees with the reference solution on its cases;
- no oracle's normalized AST body equals the reference solution's (reuse `_normalize_body` from `tests/test_no_leaks.py`);
- each oracle on its cases runs in under 2 s.

### Exemplar C: a practice notebook (`course/04-collections/03-dicts-practice.ipynb`)

Tested in a scratch run against `pylearn.check`. It uses only loops, tuples, lists and dicts, all taught by this point.

- **Warm-up** (keep): `present` with the two scrambled lines. Fine as a 30-second start.
- **Core:** `index_by_city(people: list[tuple[str, str]]) -> dict[str, list[str]]` maps each city to the names of the people who live there, in input order.

  ```python
  check(index_by_city, [("Ada", "Paris"), ("Bea", "Rome"), ("Cy", "Paris")],
        expect={"Paris": ["Ada", "Cy"], "Rome": ["Bea"]})
  check(index_by_city, [], expect={})
  check(index_by_city, [("Ada", "Oslo")], expect={"Oslo": ["Ada"]})
  ```

  Hints:
  1. A dict value can be a list, and each city needs its own list.
  2. Walk the pairs. The first time you see a city, give it an empty list. Every time, append the name.
  3. A skeleton:

     ```python
     for name, city in people:
         if ___ not in index:
             index[city] = ___
         index[city].___(name)
     ```

  The reference body is 5 lines.
- **Debug:** the lesson's real mistake, planted.

  ```python
  def group_names(people: list[tuple[str, str]], cities: list[str]) -> dict[str, list[str]]:
      groups = dict.fromkeys(cities, [])
      for name, city in people:
          groups[city].append(name)
      return groups


  check(group_names, [("Ada", "Paris"), ("Bea", "Rome")], ["Paris", "Rome"],
        expect={"Paris": ["Ada"], "Rome": ["Bea"]})
  ```

  The failure message shows `{'Paris': ['Ada', 'Bea'], 'Rome': ['Ada', 'Bea']}`, which is the clue. The prompt reads: "This function has the bug from the lesson's Common mistake. Find it, say why it happens in one sentence, then fix it."
- **Stretch:** `merge_counts(first, second) -> dict[str, int]` returns a new dict and leaves both inputs unchanged.

  ```python
  check(merge_counts, monday, tuesday, expect={"tea": 2, "coffee": 4, "juice": 1})
  assert monday == {"tea": 2, "coffee": 1}, "merge_counts changed its first argument"
  ```

- **Reflect** (keep): "In one sentence: when is `data[key]` the wrong lookup?"

`solutions/course/04-collections/03-dicts.py` gets `present`, `index_by_city`, the fixed `group_names` (build a new list per key), and `merge_counts`.

### Exemplar D: a milestone project (`use-cases/02-command-line/project`, csvtool)

The README has one section per milestone. Each section covers: what's new, the course units it uses (as links), the exact behavior, and one **Decide** question the learner answers in a `DECISIONS.md` they keep in the project folder.

| Milestone | Behavior (tests in `tests/test_m<N>_*.py`) | Uses | Decide |
| --- | --- | --- | --- |
| M1 count | `csvtool count FILE` prints the number of data rows. A header-only file prints `0`. | 14-files/03-csv, 13-modules/02-main | Is a blank trailing line a row? |
| M2 columns | `csvtool columns FILE` prints the header names, one per line, numbered from 1. | 04-collections | 0- or 1-based numbering for humans? |
| M3 filter | `count --where COL=VALUE`, repeatable, all must match. An unknown column exits with code 2 and `error: no column 'x'` on stderr. | 06-errors, 05-functions/05 | Case-sensitive matching? |
| M4 bad input | A missing file, an empty file, or a ragged row (fewer fields than the header) each gives a clear stderr message and exit code 2, never a traceback. | 06-errors/02-raise, 11-classes/06-custom-exceptions | Skip ragged rows with a warning, or fail? |
| M5 summary | `csvtool summary FILE COL` prints count, min, max and mean for a numeric column. Blanks are skipped and counted. A non-number exits 2 and names the row. `--json` prints the same as JSON. | 14-files/02-json, 10-pitfalls/05-floats | `float` or `Decimal`? |

The solution grows to about 120–180 lines, with 12–20 tests across the five files.

Milestone plans for the other projects (Rick may reorder; don't add scope beyond these):

| Project | M1 | M2 | M3 | M4 | M5 |
| --- | --- | --- | --- | --- | --- |
| tidy | plan moves by suffix | `--dry-run` prints the plan, moves nothing | apply moves; a name collision becomes `name (1).ext` | `undo` reads `undo.json` and restores | skip hidden files; print a summary table |
| expenses | parse rows into a dataclass with `Decimal` amounts | category rules from a JSON file; unmatched → `other` | monthly totals by category | bad rows reported with line numbers, not fatal | budget file → over-budget report; the chart stays |
| price-watch | parse a price from the fixture | parse 3 more fixtures (`$1,299.00`, `1.299,00 €`, missing price → `None`) | a watchlist JSON plus SQLite history | alert when the price drops by at least X% vs the last seen | fetch with `httpx` using `MockTransport` in tests; a polite delay between requests |
| notes-api | create, list, read (exists) | update and delete; 404s | validation (title 1–100 chars) → 422 | `?q=` search, `limit`/`offset` paging | tags, and filter by tag; the store sits behind a `Protocol` with an in-memory fake in tests |
| ticket-triage | `classify_all` + `accuracy` with `FakeClient` (exists) | confusion matrix and per-label precision/recall | retry with backoff on a client that fails N times; give up → `"unknown"` | classify concurrently with a bound on in-flight calls | cache labels on disk keyed by a text hash. Optional real-provider adapter behind the `Client` protocol, never called in tests |

**Capstone** (item J7, new folder `use-cases/capstone/project/`): a reading-list tool. It has a CLI and a small HTTP API over one SQLite store, imports a CSV, and runs a background job that fills in titles from a mocked HTTP lookup. It has a test file per milestone and a `DECISIONS.md`. Each milestone names the units it combines. Six milestones, about 300–450 lines of solution. **(Rick decides)** the topic before J7 starts. If PROGRESS-5 has no decision recorded when you reach J7, stop with a blocker.

---

## 5. Guard specs (item S4)

All new checks share `tests/_text.py`:

```python
import re

def normalize(text: str) -> str:
    """Lowercase, treat - and _ as spaces, collapse whitespace."""
    return re.sub(r"\s+", " ", re.sub(r"[-_]", " ", text.casefold())).strip()
```

Pending paths live in **one** file, `docs/maintainers/status.md`, under one heading per guard. Use the same exact path list shape the old status files used. Each new test does `pytest.xfail` with `strict=True` for listed paths only, so a fixed path that is still listed fails and forces you to remove it. Delete the four old status files and update the links that pointed at them.

| Guard | File | Rule |
| --- | --- | --- |
| G1 statement | `tests/test_challenge_notebooks.py` (new) | First cell ≥ 60 words of prose. Contains `**Difficulty:**`, `**Target:**` and `**Constraints.**`. No `**Pattern:**`. No "Solutions:" line. |
| G2 template text | same | Normalized markdown contains none of: `solve the stub`, `lesson prompt`, `padding asserts`, `asserts encode examples`, `edges follow in the same cell`, `see asserts for`, `see the walkthrough`. The problem slug in its hyphenated form does not appear in prose. |
| G3 hints | same | `## Hints` has ≥ 3 `<details>`. The last one has a code fence containing `___`. |
| G4 stub | same | The stub is typed. No `*args, **kwargs` signatures in learner code. |
| G5 no oracles | same | No `def` or `class` whose name, normalized, starts with `brute`, `_brute`, `slow`, `_slow`, `ref`, `_ref`, `oracle` or `_oracle`. No in-cell `random.Random` unless the notebook's only random use is a property check (allow it with a markdown cell tagged `property-check` that says what property it checks). |
| G6 real checks | `tests/test_challenge_checks.py` (edit) | Count asserts whose AST contains a `Call` to the stub's name (or the class under test), plus 1 per `cross_check(` or `cross_check_ops(` call. Need ≥ 8. Fail on any constant assert (D3). Normalize before checking `no-random` reasons. Ban `not required` and `this round` in them. Expected `no-random` count after round 5: 0. |
| G7 walkthrough link | same | The only link into `solutions/` is under `## After you pass` and points at the matching `.md`. |
| G8 hint leak | `tests/test_practice_hints.py` (new) | For every course and pattern practice notebook, no hint code (inline or fenced), whitespace removed, equals or contains a reference-solution function body (whitespace removed, at least 12 chars). |
| G9 practice shape | same | Headings in order: `Warm-up`, `Core`, `Debug` (from `02-strings` on), `Stretch`, `Reflect`. The Core or Stretch reference body has at least 4 statements (count nested `ast.stmt` nodes, excluding the docstring), from `01-basics` on. |
| G10 raises must raise | `tests/test_lessons.py` (edit) | After a fresh run, every cell tagged `raises-exception` has an `error` output. |
| G11 freshness | same | Compare `execute_result` `text/plain` and error `ename` too, not only stdout. |
| G12 stale words | `tests/test_lesson_structure.py` (edit) | Normalized learner markdown in lessons doesn't contain `predict cell`. |
| G13 boilerplate | `tests/test_no_boilerplate.py` (edit) | `MAXIMUM_NOTEBOOKS = 2`. Add practice notebooks and challenge notebooks to `PATTERNS`. Normalize sentences before counting. |
| G14 constant asserts anywhere | `tests/test_no_boilerplate.py` (edit) | No constant assert in any learner notebook or `exercise/` file. |
| G15 tutor files | `tests/test_ai_instructions.py` (edit) | `AGENTS.md` names `docs/maintainers/authoring.md`. `tools/learner_mode.py on --root <tmp>` writes `.cursorignore` containing `solutions/` and a rule with `alwaysApply: true`; `off` removes both. `.gitignore` lists both paths. |
| G16 projects | `tests/test_projects.py` (new) | Every `use-cases/*/project` has ≥ 4 `tests/test_m<N>_*.py` files, ≥ 2 tests in each, and a README with one `## M<N>` heading per test file and a **Decide** line in each. |

Expected counts when S4 lands (sanity check, from the review scripts):
- G1: 68
- G2: about 68
- G3: 68
- G4: 25
- G5: 29
- G6: 30 (constant asserts in 13–42) + 26 (excuses)
- G8: 29
- G9: most of the 73 course practices
- G10: 2
- G12: 7
- G16: 6

If your numbers are far off, check the guard before you move on.

---

## 6. Quality bar

**Challenge notebook** (Exemplar A):
- [ ] A learner who has never heard the problem's name can start it from cell 0.
- [ ] Examples have reasons. Constraints have sizes. The target complexity is stated.
- [ ] "Before you code" questions are about this problem and lead toward the key insight without stating it.
- [ ] Three hints: pattern and idea → approach in words → skeleton with blanks. The pattern name appears in no earlier cell.
- [ ] Typed stub. At least 8 asserts that call it, plus `cross_check` (or a property check for problems with many right answers).
- [ ] You wrote one deliberately wrong variant (a classic bug from the walkthrough's Common bugs) and confirmed a check catches it. Record it in the notes.
- [ ] The walkthrough link appears only under `## After you pass`.

**Practice notebook** (Exemplar C):
- [ ] Core needs a loop, a branch, or two ideas together. The reference body is at least 4 statements.
- [ ] Debug plants the lesson's own Common mistake, and the check message makes the symptom visible.
- [ ] Stretch is a small realistic task, not a one-liner.
- [ ] No hint contains a full answer.
- [ ] Only concepts taught by this point are used (`docs/maintainers/concepts.md`; add a row when you rely on a concept the ledger lacks, for example `enumerate`).

**Lesson fix** (section X items):
- [ ] Every claim has an evidence cell, and the evidence agrees with the prose.
- [ ] Cells tagged `raises-exception` raise.
- [ ] No sentence is there only to add words.
- [ ] `depth_report.py` is still in band. If a cut drops a lesson below its band, add explanation or evidence, not filler.

**Project milestone** (Exemplar D):
- [ ] The README section says what's new, which units it uses (links), the exact behavior including errors, and one Decide question.
- [ ] The test file covers the happy path, one edge case and one error path.
- [ ] The milestone's solution passes with `PYLEARN_SOLUTIONS=1`, and the stubbed version fails cleanly (`NotImplementedError` or a failing assert, never an import error).

---

## 7. Never do these

- Don't weaken, skip or delete a test. Don't lower a threshold. Don't add `xfail`, `skip` or `noqa` to get past a check. The only `xfail`s allowed are the paths in `docs/maintainers/status.md`, and that list only shrinks.
- Don't satisfy a count with filler: no constant asserts, no repeated asserts, no sentences there only for word count, no hyphen or spacing tricks around a banned phrase. If a guard is wrong, fix the guard in its own commit and explain why in the item notes.
- Don't hand-write notebook outputs.
- Don't put a solution, an oracle or a whole-body hint in a learner file.
- Don't solve a challenge problem inside `patterns/`.
- Don't add third-party packages to `course/`, `patterns/`, `internals/` or `src/pylearn/`.
- Don't commit `.cursorignore`.
- Don't edit files in `docs/maintainers/review/` other than `PROGRESS-5.md` and the final `ROUND5-REPORT.md`.
- Don't push, open PRs, or change CI secrets.

---

## 8. Final gate (items F1–F3)

The run is done only when all of these hold:

- `docs/maintainers/status.md` lists nothing, and the suite reports **0 xfail**.
- `uv run pytest -n 4`, `PYLEARN_SOLUTIONS=1 uv run pytest -n 4 course use-cases`, `uv run ruff check .` and `uv run ruff format --check .` all pass after a fresh `uv sync --locked --all-groups`.
- `tools/depth_report.py` shows 0 LOW and 0 HIGH.
- A second run of the full suite leaves `git status` clean (no files written into the repo).
- `ROUND5-REPORT.md` exists. It covers:
  - what changed, with counts: the CRITIQUE-5 numbers before and after;
  - each blocker and how it was resolved;
  - each guard you changed and why;
  - deviations from this runbook;
  - the 10 challenge notebooks, 10 practices and 2 projects you think are weakest, so Rick reviews those first.
