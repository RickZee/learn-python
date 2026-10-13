# Review, round 5: what the green suite still lets through

Reviewed 2026-10-12 on `main` at `0974758`. This replaces the uncommitted `CRITIQUE-4.md` draft from the same day. Companion files: [RUNBOOK-5.md](RUNBOOK-5.md) (how to fix it) and [PROGRESS-5.md](PROGRESS-5.md) (the work list). Earlier rounds: [CRITIQUE-3.md](CRITIQUE-3.md), [ROUND4-REPORT.md](ROUND4-REPORT.md).

## Verdict

The harness runs well. On a clean clone, `uv sync --locked --all-groups` works, `pytest -n 4` gives **919 passed**, `PYLEARN_SOLUTIONS=1 pytest course use-cases` gives **23 passed**, and `ruff check .` is clean. Course and internals lessons mostly teach the mechanism and its cost. Round 4 fixed the pattern lessons and the walkthroughs.

Two things are wrong under that green result.

1. **Some guards are being gamed.** 30 challenge notebooks reach the 8-check minimum with 126 `assert 0 == 0` lines. 26 notebooks keep the banned "no oracle" excuse by writing "brute-force" with a hyphen, which the exact-string ban misses. `ROUND4-REPORT.md` and `PROGRESS-4.md` (O1, O2) report the oracle work as done. It isn't.
2. **The pages learners use most were never covered by a guard.** These are the challenge notebooks, the size of practice exercises, the six projects, and which AI mode a learner starts in.

Fix both before the launch posts send people here.

## How I checked

- Fresh clone, full suite, solutions run, `ruff check`, `ruff format --check`.
- Scripts over every notebook. They compared `raises-exception` tags with real error outputs, found duplicate and near-duplicate code cells, found sentences repeated across lessons, and found references to sections that were removed.
- Compared every practice hint with the reference solution under `solutions/`.
- Measured the size of each reference solution and found which function is the "Core" item in each practice.
- Scanned all 68 challenge notebooks for: a problem statement, template phrases, stub signatures, oracles in learner cells, constant asserts, and `no-random` reasons.
- Read samples end to end: decorators, contextlib, dates-and-times, GIL, the dicts practice, Two Sum, Edit Distance, the six projects, and the AI setup files.

## 1. The challenge notebooks (highest severity)

The walkthroughs are good. The notebooks learners actually open are not.

| Signal | Count (of 68) | Where |
| --- | --- | --- |
| No problem statement. The first cell is under 60 words: "Solve the stub.", or Two Sum's "Return the answer described in the lesson prompt" (there is no lesson prompt). | **68** | all |
| The only hint is "See the walkthrough". The walkthrough lives in `solutions/` and gives the full algorithm. 65 has no hints at all. | **67 + 1** | all |
| Constant asserts (`assert 0 == 0  # padding check 0 for …`) that only exist to reach 8 checks | **30 notebooks, 126 asserts** | 13–42 |
| Fewer than 8 real asserts once those are removed | **30** | 13–42 (some have only 2) |
| `no-random` reason is the banned generic excuse with a hyphen ("compact brute-force oracle is not required for this round") | **26** | 13, 14, 16–19, 22–25, 27–42 |
| Harness text shown to learners ("Asserts encode examples for …", "Padding asserts keep the suite at eight checks for …", "Edges follow in the same cell …") | **25** | 43–64, 66–68 |
| Prompts built from the slug ("What pattern fits edit-distance?", "Which edge breaks edit-distance?") | **26** | 43–68 |
| Stub is `def f(*args, **kwargs)` (no parameter names or types) | **25** | 43–64, 66–68 |
| A complete, correct reference implementation (`brute`, `_brute_*`, `_BruteTimeMap`) sits in the learner's cell | **29** | 02–08, 10, 12, 43–47, 49–51, 53, 54, 56–58, 60–65, 68 |

What this means for a learner:

- A beginner can't start these problems. They are LeetCode titles with no statement.
- The hints jump from nothing straight to the whole algorithm. The AI tutor is told not to read `solutions/`, so it can't give a middle hint from the walkthrough either.
- 29 notebooks hand over a working answer. A learner can `return brute(...)` and pass every check except, sometimes, the scale check. In Edit Distance, `_brute_edit` is the memoized recursion, which is the target-complexity solution.
- 30 notebooks are barely tested, so half-right answers pass.

The guard in `tests/test_challenge_checks.py` counts asserts, but it doesn't look at what they assert. It bans the excuse as one exact string. RUNBOOK-2's quality bar asked for "a randomized cross-check against an in-notebook brute force". That rule produced the leaked oracles, and RUNBOOK-5 reverses it.

## 2. Practice is mostly one-liners, and a hint often is the answer

| Signal | Value |
| --- | --- |
| Course practice notebooks | 73 |
| …whose **Core** reference solution is at most 2 lines | **42 (58%)** |
| Course reference-solution functions | 223 |
| …median body length | **1 line** |
| …one-line bodies | **132 (59%)** |
| Pattern reference functions, median | 5 lines (fine) |
| Practice notebooks where a hint contains the reference body, character for character | **29** |

Example: in `course/04-collections/03-dicts-practice.ipynb`, the warm-up is `return key in data`, a two-line "Parsons" puzzle. The core is `return data.get(key, default)`, and its third hint prints exactly that line. The stretch is `setdefault`. Each item checks that the learner knows one method name, and none makes them combine two ideas.

Round 4 item T2 rewrote 27 stretches, but many stretches are still one line: 01-basics/01–02, 02-strings/02–05, 05-functions, 07-iteration, 13–14. This works against the course promise of in-depth understanding. It also works against the tutor's rule to guide rather than solve, because the notebook solves it first.

The 29 notebooks:
`00-start/02`, `01-basics/01`, `02-strings/01–05`, `04-collections/01, 03, 04, 05, 06`, `05-functions/02`, `07-iteration/01, 03`, `08-collections-module/01, 04, 06`, `10-pitfalls/02, 03, 05`, `11-classes/02, 05`, `13-modules/01`, `14-files/01, 02, 04`, `17-concurrency/02`, `18-tooling/02`.

## 3. The projects are much smaller than the README says

The README and `use-cases/README.md` promise "six deep builds" of 90–120 minutes each.

| Project | README spec | Tests | Reference solution |
| --- | --- | --- | --- |
| tidy | 2 sentences + 3 one-line milestones | 3 | 22 lines |
| csvtool | 1 sentence ("Count the data rows in a CSV.") | 2 | 22 lines |
| notes-api | 2 sentences | 1 | 43 lines |
| expenses | 1 sentence | 2 | 31 lines |
| ticket-triage | 2 sentences | 2 | 33 lines |
| price-watch | 1 sentence | 2 | 25 lines |
| **All six** | | **12** | **~180 lines** |

Only tidy has milestones, and each is one line with no tests of its own. None of the projects has a real spec or a design decision for the learner, and there's no capstone that ties the course together.

## 4. In Cursor, a learner starts in authoring mode

- **Cursor** reads `AGENTS.md`, which begins "In most sessions you are authoring course content." The tutor rule (`.cursor/rules/practice-tutor.mdc`) is `alwaysApply: false`, so the agent decides whether to load it. A learner who types "my dicts practice fails, fix it" gets an agent whose standing instructions are to edit content.
- **Nothing in Cursor blocks reading `solutions/`.** There's no `.cursorignore`. Committing one would also block the authoring agent, which has to write solutions. So it has to be something the learner turns on (see RUNBOOK-5). Cursor's docs say `.cursorignore` covers Agent, Tab, Inline Edit and @-mentions, but not the agent's terminal or MCP tools.
- **Claude Code is already right.** The learner profile turns on the tutor and blocks reads of `solutions/`. The `Read(...)` rule doesn't stop `cat solutions/...` through Bash; say so in the AI setup doc.

## 5. Correctness slips the suite doesn't catch

| Where | Problem |
| --- | --- |
| `course/14-files/05-dates-and-times-lesson.ipynb` | The prose and the Check-yourself answer say comparing naive and aware datetimes "raises TypeError". The evidence cell does `naive == aware` and prints `False`. Equality doesn't raise; only ordering (`<`) does. The cell is tagged `raises-exception` but doesn't raise. The "Deep dive" line has no link. |
| `course/16-decorators/01-decorators-lesson.ipynb` cells 13–14 | The common-mistake cell is tagged `raises-exception`, prints `None`, and never raises. The next cell talks about "the traceback's last line". |
| Same lesson, Why section | Contains the stray sentence "Equal hashes are not the topic here; identity of the callable is." It says each wrapper frame "appears in a traceback unless you use wraps-aware tooling", which wrongly suggests `wraps` removes frames. Stacking order is described but never run. Cell 10 repeats cell 4. |
| 7 cells | Refer to "the predict cell", which the teach-first flow removed: `course/00-start/02-practice-lesson` #9, `course/09-recursion/02-structures-lesson` #9, `internals/10-bytecode/01-bytecode-lesson` #7 and #10, `internals/11-memory/01-refcount-lesson` #10, `internals/12-gil/01-gil-lesson` #5 and #10. |
| 3 lessons, including dates-and-times | Shared padding sentence: "That cost shows up when the input grows: each extra unit of work multiplies wall time or memory…" |
| `course/12-data-model/03-contextlib-lesson.ipynb` | The same `marked()` generator is defined in five cells. In total there are 35 near-duplicate code-cell pairs across 17 lessons. Mistake/fix pairs are fine. Repeated evidence is padding: `09-recursion/04-memoization`, `06-errors/04-else-finally`, `09-recursion/02-structures`, `17-concurrency/04-race-conditions`. |
| `course/15-testing/02-mocking-practice.ipynb` | Writes `_title_demo.txt` into the course folder and deletes it only after the checks pass. Every unsolved run, including CI, leaves the file behind. Round 4 S5 deleted the file but not the cause. |

Why the suite missed these:

- nbclient *allows* an error in a `raises-exception` cell but doesn't require one.
- The freshness test compares only stdout.
- The banned-phrase lists are exact strings.

## 6. Learners have no way to take updates

Learners edit practice notebooks in place in a clone. The course will keep changing after launch. The first `git pull` that touches a notebook they edited is a merge conflict in JSON. No learner doc mentions forking, branches, or updating.

## 7. Codespaces is still untested

`DOCS-REPORT.md` and `ROUND4-REPORT.md` both list it as untested. The image is the moving `python:3` tag, `postCreateCommand` doesn't use `--locked`, and the README badge sends launch traffic there first.

## 8. Smaller items

- **CI masks a hang.** Under `-n 4`, `12-data-model/02-context-managers-lesson` waited 120 s for a kernel to start before the retry passed. Alone it runs in about 1 s. `startup_timeout=120` makes every retry slow.
- **Formatting.** `ruff format --check` would reformat 407 files. Learners read lesson code as examples.
- **Coverage gaps.** No course lesson uses `:=`, `yield from`, `functools.partial`, `reduce`, `singledispatch`, or a profiler. `16-decorators` is one 30-minute lesson. `enumerate` is taught in the zip lesson but is missing from `concepts.md`.
- **Challenges index.** `challenges/README.md` links only to problem 01. There's no table of the 68 problems with pattern, difficulty and target complexity.
- **Placement test.** `course/00-start/00-skip-test.ipynb` sits first in the beginner's first unit, and learners grade it themselves on paper.
- **Launch hygiene.** There's no `CONTRIBUTING.md`, no issue templates, no repo topics, no social preview, and no README image of the tutor at work.
- **Housekeeping.** Four status files all say "Empty". `ROUND4-REPORT.md` says "Renamed `challenges/` → `challenges/`". AGENTS.md says never to link learners to `solutions/`, but every problem notebook does.

## What not to do

- Don't add problems, units or explore pages this round.
- Don't loosen a guard to get green. If a guard is wrong, fix the guard in its own commit and say why in PROGRESS-5.
- Don't reopen the lesson flow or the folder layout. Both are settled.

## Success looks like

- A beginner opens any challenge problem, knows what to build, gets three hints before any spoiler, and can't copy an oracle.
- A practice notebook makes the learner combine ideas and fix a planted bug.
- A project takes an afternoon and ends with something worth showing.
- Cursor and Claude both start as tutors for learners and as authors for you.
- A learner can pull your next update without a merge conflict.
- Every guard checks what it claims to check.
