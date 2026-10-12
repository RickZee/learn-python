# Review: learn-python repo

Reviewed 2026-10-10 against the working tree (not just the initial commit). Companion file: [AGENT_PLAN.md](AGENT_PLAN.md) has the step-by-step fixes, for Cursor, Claude Code, or any coding agent.

## Verdict

The skeleton is good: consistent lesson/practice pairs, runnable checks, a sensible order, a strong challenge checklist, and current tool choices. The content on top of it is too thin to teach, and parts of it are wrong. Three practice notebooks can't be passed even with correct code, two lessons show output that a real run doesn't produce, and nothing in the repo checks for either kind of error. The terse style suits an experienced programmer skimming for Python idioms. It does not yet work for a beginner, and the challenges section mostly re-runs problems the pattern lessons have already solved.

## How I checked

- Ran all 151 notebooks in a real Jupyter kernel (CPython 3.14.7 via `nbclient`). That's 77 lesson-type notebooks and 74 practice notebooks.
- Wrote reference solutions for all 74 practice notebooks, spliced them in, and ran them in the kernel. A correct solution should pass every check.
- Re-ran everything on CPython 3.10 to test the "requires 3.14" claim.
- Ran `ruff`, checked every relative link, and compared the challenge problems with the pattern-lesson practice.
- Compared the design with current teaching research and with the 2025–26 state of Python and of timed challenges (sources at the end).

## What works

- **Structure.** Lesson and practice share a number, and `lesson` sorts before `practice`, so the order is obvious. The navigation docs agree with each other. None of the relative links are broken.
- **Executable practice.** Every exercise is a function with checks, so learners get feedback right away. The function-shaped tasks are also easy to test automatically, which most of the fixes below depend on.
- **Good pitfalls.** Mutable defaults, aliased grid rows, and `is` vs `==` are the right misconceptions to target.
- **Modern idioms.** `match`, `X | None`, built-in generics, `pathlib`, `Decimal` for money, `secrets.compare_digest`, `tomllib`, and `forkserver`/`spawn` awareness.
- **Challenge process advice** (`challenges/guide.ipynb`) is accurate: restate, brute force first, name the data structure, narrate, give the complexity, check edge cases, and re-implement the next day. The core list matches the usual Blind 75 / Grind 75 core.
- **Current tool picks.** The use-case pages recommend current tools: FastAPI, pydantic, polars, httpx, Textual, uv, and a Python 3.14 runtime on Lambda, which [AWS added in Nov 2025](https://aws.amazon.com/about-aws/whats-new/2025/11/aws-lambda-python-314).

## Verified defects

Severity reflects impact on a learner.

| # | Sev | Where | Problem | Evidence |
|---|---|---|---|---|
| 1 | Critical | `course/07-comprehensions/01-comprehensions-practice.ipynb` | `assert even_squares(3) == [0]` is wrong. `range(3)` contains 0 and 2, so the answer is `[0, 4]`. A correct solution fails. | Reference solution fails only on this line. |
| 2 | Critical | `challenges/problems/14-merge-two-sorted-lists.ipynb` | Expects `[1, 1, 2, 3, 4]`, which drops a 4. The merge of `[1,2,4]` and `[1,3,4]` is `[1, 1, 2, 3, 4, 4]`. | Same. |
| 3 | Critical | `course/23-concurrency/03-async-lesson.ipynb`, `03-async-practice.ipynb` | `asyncio.run()` raises `RuntimeError: asyncio.run() cannot be called from a running event loop` inside Jupyter, because the kernel already runs a loop ([ipykernel #548](https://github.com/ipython/ipykernel/issues/548)). The lesson crashes, and the practice can't pass. | Reproduced in the kernel. |
| 4 | High | Saved outputs | The async lesson's saved output `[3, 7]` can't come from a kernel run. `21-modules/02-main-lesson` shows `this file is library`, but a notebook prints `program`. These outputs weren't produced by running the notebooks. The other lessons' saved outputs do match a fresh run (apart from machine-specific values like CPU count), but nothing enforces that. | Saved and actual output differ. |
| 5 | High | `21-modules/02-main-*` | `__name__` is always `"__main__"` in a notebook, so the import-vs-run lesson can't be shown there. The practice is a string comparison. | Same run. |
| 6 | High | `15-stacks/01-parentheses-lesson.ipynb` | Defines `pairs` and never uses it. The code pops on every closing bracket without checking the match or whether the stack is empty, so it shows an incorrect algorithm: it accepts `"(]"` and crashes on `")"`. | Read and traced. |
| 7 | High | `01-basics/01-names-practice`, `03-booleans-practice`, and every practice in 01–04 | Both named notebooks need `if`, which isn't taught until `04-control-flow`. The names lesson prints `NoneType`, but the practice wants `"none"`, with no hint. More broadly, every practice from the very first one asks the learner to write a `def … return` function, but functions aren't taught until `05-functions`. Type hints (`tuple[int, int]`, `int \| None`) appear from the second practice and are never explained. | Sequencing read. |
| 8 | High | `17-graphs/01-islands-lesson`, `12-two-pointers/03-container-lesson`, `14-binary-search/02-rotated-array-lesson` | The code only prints the input or the first state. The pattern never runs. | Read. |
| 9 | High | `24-testing/01-unittest-practice` | The exercise is `is_even`. The learner never writes a test. | Read. |
| 10 | High | `23-concurrency/02-processes-practice` | The exercise is `runner_for("cpu") == "process"`, a string lookup that doesn't use processes. | Read. |
| 11 | High | `22-files/*` | A "files" unit that never opens, reads, or writes a file. There's no `open`, `with`, or `encoding`. | Read. |
| 12 | Medium | Repo | No `pyproject.toml` or lock file, and `.venv` is gitignored. `docs/setup.md` says `source .venv/bin/activate`, but nothing creates the venv, so a fresh clone can't follow setup. The local `.venv` only has ipykernel and nbclient. | `ls`, `.gitignore`. |
| 13 | Medium | Git | Everything except `.gitignore`/`LICENSE` is untracked. The only commit is "Initial commit". A large agent-driven refactor would have no baseline to diff or roll back to. | `git status`. |
| 14 | Medium | 7 practice notebooks | Before they're solved, they fail with `TypeError`/`AttributeError` (`'NoneType' object is not iterable`) instead of a clear "not done yet". Examples: `09-pitfalls/02`, `10-classes/01`, `11-hash-maps/02`, `12-two-pointers/02`, `challenges/problems/02, 04, 15`. | Kernel run. |
| 15 | Medium | ~150 notebooks, README, setup | "Python 3.14" is hard-coded everywhere, and setup says older kernels "will reject newer syntax". Nothing uses 3.14 features. Every lesson except `use-cases/14-packaging` (`tomllib`, 3.11+) runs on **3.10**, and all practice solutions pass on 3.10. [Python 3.15.0 shipped 2026-10-09](https://blog.python.org/2026/10/python-3150-final-is-here/), so this text is now dated as well as unnecessary. | 3.10 run. |
| 16 | Medium | `course/` numbering | The language order is 01–10, then 21–24, with algorithm patterns 11–20 in between. Folder sort order contradicts the reading order. | `docs/language.md`. |
| 17 | Low | README | Mentions `scratch/basics.py` and `archive/learn.ipynb`, which don't exist. | `ls`. |
| 18 | Low | Various | The zip lesson should teach `zip(..., strict=True)` (ruff B905). The threads lesson's GIL sentence needs the free-threaded note: 3.14's `python3.14t` build is [officially supported (PEP 779)](https://pydevtools.com/handbook/explanation/what-is-pep-779/), though the GIL build is still the default. The reference `threeSum`/`merge` sort their input in place, while the course stresses not mutating inputs. | ruff, reading. |

## Design critique

### 1. Lessons show code but don't teach

The median lesson has **19 words** of explanation and **one** code cell of about 7 lines. The only instruction is "run it and read the output". That's the "Run" step of [PRIMM](https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf) (Predict, Run, Investigate, Modify, Make) with the other four steps missing. The steps the evidence supports are the ones that aren't there:

- **Predict before run.** Learners commit to an answer, then see whether they were right.
- **Worked examples with subgoal labels.** In [Morrison et al.'s study](https://www.raspberrypi.org/blog/research-seminar-cognitive-load-subgoal-labels/) of 307 students, these produced better understanding, and the effect was largest for at-risk students.
- **Parsons or faded problems between "read" and "write from blank".** [Ericson found](https://hg.gatech.edu/node/603172) these give the same learning gains as writing code, and learners finish them significantly faster.
- **Common-error demos and how to read the traceback.** None of the lessons shows an error message.

Each lesson needs a mental model, a prediction, an investigation, and a modify step. More code alone won't fix it.

### 2. Practice feedback is thin and has no way out

- Checks are bare `assert`s. A failure prints `AssertionError` with no expected-vs-got. Unsolved notebooks sometimes fail with a `TypeError` raised inside the test scaffolding.
- Course practice has no hints and no solutions. The challenges section has 5 reference solutions for 21 problems.
- Each practice is one task. There's no ramp from easy to hard (warm-up, core, stretch) and no reflection prompt.
- The checks are 2–4 example cases. They don't test edge cases systematically, they don't compare against a brute-force answer on random inputs, and nothing checks complexity. A linear scan passes the binary-search exercise.

### 3. Notebook-only hides how Python is actually run

Learners never create a `.py` file, run `python file.py`, import their own module, run `pytest` from a terminal, install a package, or read a full traceback from a script. The `__main__` lesson (#5) can't work in a notebook. The same goes for the process-pool lesson (it says so itself) and for `asyncio.run` (#3). Notebooks are fine for exploration lessons. The "writing real programs" half of the course needs `.py` files and tests.

### 4. Topic gaps

`docs/language.md` lists inheritance, `__repr__`, `classmethod`/`staticmethod`, decorators, enums, truthiness, and scopes as "named, without a folder". Those are core topics, and the bullets are their only coverage. Also missing:

- Iterators and generators (`yield`)
- Context managers and `with`
- Dataclasses
- What type hints are (they appear from the second practice onward without explanation)
- `lambda` and `sorted(key=...)`
- Format specs like `:.2f`
- `raise`, custom exceptions, `else`/`finally`
- Debugging with `breakpoint()`
- Logging and regex basics
- Virtual environments and installing packages
- `input()` and a first runnable script
- Dict and set comprehensions, generator expressions
- `itertools`/`functools`
- Late-binding closures (a classic pitfall)

### 5. The challenges section repeats the course

17 of the 21 challenge problems have **identical checks** to a course pattern practice. Only the function name changes, from snake_case to camelCase. Of the 17 matching pattern lessons, 10 show the working core of the solution to that same problem, 4 show part of it, and 3 don't run the pattern at all (#8). A learner who follows the path has seen the answer, then solved it, then meets it again as a "problem". That builds recall, not the pattern recognition the guide says it's for ("pattern recognition plus clean Python beats a random problem list").

Gaps in the challenges section:

- The guide's own pattern list includes trees, monotonic stacks, BFS, cycle detection, and level order. There's **no binary-tree problem**, no backtracking, no monotonic-stack problem, no trie, no topological sort, and no 2-D DP. None of the "After the core list" problems (Course Schedule, Daily Temperatures, Word Search, etc.) are provided.
- **Hiring rounds changed in 2025–26.** Meta's AI-enabled round, rolled out from October 2025, is a multi-file codebase exercise in three phases: fix a bug, implement a feature with an AI assistant, then optimize for larger inputs. It's scored on problem solving, code quality, verification, and communication (PracHub third-party write-up of Meta's AI-enabled round). The repo has no practice for reading unfamiliar code, debugging, or verifying AI output.
- LeetCode camelCase names go against PEP 8 everywhere else in the repo. Keep the LeetCode title in the heading and use snake_case in code.

### 6. Use cases are a catalog, not projects

The 23 fields each have a 4–24 line standard-library snippet. Step 2 of "Do this first", the "small project", usually repeats the lesson. For example, the media lesson converts RGB to HLS, and the project is to convert one RGB colour to HLS. There's no spec, starter code, acceptance tests, or milestones. No use case ever installs a listed tool, so learners never practise `uv add`, reading library docs, environment variables, or secrets. There's no AI/LLM application track, even though building with LLM APIs and agents is one of the fastest-growing reasons people learn Python now; [JetBrains' State of Python 2025](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025) explicitly recommends learning agentic AI. Depth in 5–6 fields beats a shallow pass over 23.

### 7. AI assistance can quietly replace the practice

Learners will have an AI next to every exercise: Cursor's agent and Tab completion, Claude Code, or the Claude app in another window. Practice functions have names like `twoSum` that any of them completes instantly. In a ~1,000-student field experiment, unrestricted GPT-4 access raised practice scores 48% and **lowered** exam scores 17% once the AI was removed. A hint-only tutor version avoided the harm ([Bastani et al., PNAS 2025](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)).

The repo should set that guardrail itself, for every tool, from one shared tutor text:
- **Cursor:** a project rule.
- **Claude Code:** a custom [output style](https://code.claude.com/docs/en/output-styles.md) plus a learner settings profile whose [deny rules](https://code.claude.com/docs/en/permissions.md) stop Claude's file tools from editing practice files or reading `solutions/`.
- **Claude app:** Project instructions plus the built-in [Learning style](https://engadget.com/ai/anthropic-brings-claudes-learning-mode-to-regular-users-and-devs-170018471.html).

Authoring instructions belong in `AGENTS.md`, which Cursor and [Claude Code](https://code.claude.com/docs/en/memory.md) both read, and must stay separate from tutor mode. Otherwise the tutor blocks whoever maintains the course. Inline autocomplete ignores all of these, so learners should switch it off while practising.

### 8. Repo and tooling

- **Make setup reproducible.** Add `pyproject.toml`, `uv.lock`, and `.python-version`, using the [uv Jupyter workflow](https://docs.astral.sh/uv/guides/integration/jupyter/).
- **Add CI that executes every notebook.** That would have caught #1–#4. Run the practice notebooks with solutions spliced in, and the lessons in a real kernel.
- **Teach pytest, not only unittest.** pytest is used by [53% of Python developers vs 23% for unittest](https://lp.jetbrains.com/python-developers-survey-2024/).
- **Commit before refactoring** (#13).

## Fit by audience

| Audience | Fit today | What blocks them | What would make it work |
|---|---|---|---|
| **Never programmed** (career changer, non-technical professional) | Poor | 19-word lessons, unexplained type hints, concepts used before they're taught, no error-reading, cryptic failures, wrong asserts, a uv/kernel setup with no fallback, no solutions | PRIMM lesson template, an "explain more" layer, a check helper with plain-English failures, hints and solutions, a first-program lesson in a `.py` file, a setup troubleshooting page. Half of Python developers have <2 years of professional experience ([State of Python 2025](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025)), so this audience is large. |
| **Knows another language** | Fair | The terse style suits them, but the topics they need most are missing (data model, iterators/generators, context managers, decorators, dataclasses, typing, packaging, pytest, asyncio done properly). There's no skip test, so they wade through basics. | A diagnostic "skip test" notebook, an "if you know Java/JS/C#" contrast note per unit, and a solid Part 2 (real programs in `.py` files). |
| **Challenge prep** (senior/lead) | Fair | Answers revealed before practice, identical repeats, missing trees/backtracking/heaps/topo-sort, weak tests, only 5 solutions, nothing for AI-enabled or debugging rounds | Pattern lessons on *sibling* problems, unseen challenge problems with constraints, hint ladders, perf and randomized tests, full solutions, and a codebase-round exercise. |
| **Wants to build something** | Poor | Use cases are catalog pages, never touch real libraries, and have no project specs | Six deep projects with spec, milestones, starter package, acceptance tests, and a reference solution, including an AI/LLM app. |
| **Instructor running a cohort** | Poor | No objectives, time estimates, answer keys, or facilitator notes | Objectives and time per lesson, the `solutions/` folder, a facilitator guide. |

**Decide the primary audience and say so in the README.** The voice, the senior-challenge framing, and the use-case breadth point to experienced professionals. That's a fine choice. Beginners can then be served with a progressive-disclosure layer instead of a rewrite. If beginners are a real target, Phase 3 of the plan isn't optional.

## Fix order

1. Commit the current tree. Fix #1–#3 and #6 (wrong checks, crashing async, wrong algorithm).
2. Add `pyproject.toml`/`uv.lock` and CI that executes everything, then regenerate all saved outputs from real runs.
3. Add a `solutions/` folder and the check helper with clear failure messages.
4. Fix sequencing (#7) and replace the hollow exercises (#5, #9, #10, #11, #8).
5. Rework the lesson template (PRIMM, subgoals, Parsons warm-up, error demo).
6. Restructure: language course in one numbered sequence, patterns in their own folder, challenge problems kept unseen.
7. Fill topic gaps and add the missing challenge pattern families.
8. Turn 5–6 use cases into real projects, including an AI/LLM app.
9. Add audience paths, a skip test, and tutor mode for Cursor, Claude Code, and the Claude app. The AI setup itself comes earlier, in Phase 0.

## Sources

- [Python 3.15.0 final release (python.org blog)](https://blog.python.org/2026/10/python-3150-final-is-here/)
- [Python news, October 2026 (Real Python)](https://realpython.com/python-news-october-2026/)
- [PEP 779 and free-threaded Python in 3.14 (pydevtools)](https://pydevtools.com/handbook/explanation/what-is-pep-779/)
- [ipykernel issue #548: asyncio.run in a running loop](https://github.com/ipython/ipykernel/issues/548)
- [uv: using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)
- [nbmake (pytest plugin for notebooks)](https://pypi.org/project/nbmake/)
- [PRIMM pedagogy summary (Raspberry Pi Foundation)](https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf)
- [Subgoal labels and cognitive load (Raspberry Pi Foundation)](https://www.raspberrypi.org/blog/research-seminar-cognitive-load-subgoal-labels/)
- [Ericson: Parsons problems dissertation (Georgia Tech)](https://hg.gatech.edu/node/603172)
- [Without guardrails, generative AI can harm education (Wharton)](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)
- [The State of Python 2025 (JetBrains)](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025)
- [Python Developers Survey 2024 results (JetBrains/PSF)](https://lp.jetbrains.com/python-developers-survey-2024/)
- Meta's AI-enabled timed challenge (PracHub, third-party write-up)
- [AWS Lambda adds Python 3.14](https://aws.amazon.com/about-aws/whats-new/2025/11/aws-lambda-python-314)
- [Cursor rules documentation](https://cursor.com/docs/rules)
- [Claude Code: CLAUDE.md, AGENTS.md and rules](https://code.claude.com/docs/en/memory.md)
- [Claude Code: output styles (Learning, custom)](https://code.claude.com/docs/en/output-styles.md)
- [Claude Code: permission deny rules](https://code.claude.com/docs/en/permissions.md)
- [Claude's learning mode for all users (Engadget)](https://engadget.com/ai/anthropic-brings-claudes-learning-mode-to-regular-users-and-devs-170018471.html)
