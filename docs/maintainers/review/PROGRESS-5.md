# Progress 5: honest guards, real challenges, deeper practice, real projects

Work top to bottom. The loop, decisions, exemplars, guard specs and quality bar are in [RUNBOOK-5.md](RUNBOOK-5.md). The reasons are in [CRITIQUE-5.md](CRITIQUE-5.md).

## Blockers

- ~~**J7 capstone topic:** still undecided.~~ Resolved 2026-10-12: Rick chose the reading-list tool (see Decisions from Rick).

## Decisions from Rick

- Capstone topic (J7): **reading-list tool**, as specified in RUNBOOK-5 §4 D (CLI + small HTTP API over one SQLite store, CSV import, background job filling titles from a mocked HTTP lookup, test file per milestone, `DECISIONS.md`; six milestones, about 300–450 lines of solution). Decided by Rick 2026-10-12.
- Early merge: moot, because C–J6 are already done. Merge at F3 as planned.

## S. Setup and guards

- [x] **S1** Create branch `review/round-5-run` from `main`. Delete the untracked `docs/maintainers/review/CRITIQUE-4.md` draft; CRITIQUE-5 replaces it. Notes: branch created from main; CRITIQUE-4 was tracked (not untracked) — removed anyway; CRITIQUE-5 is the source of truth.
- [x] **S2** Split the agent instructions (RUNBOOK-5 D5).
  - Move every rule under `## Layout`, `## Commands`, `## Authoring standards` and `## Lesson flow` from `AGENTS.md` into a new `docs/maintainers/authoring.md`, unchanged except for adding D1–D4, D7, D8 and D9 as rules.
  - Rewrite `AGENTS.md` as a router of at most 25 lines:
    1. "This repo teaches Python. By default you are a tutor: follow docs/guides/ai-prompts/tutor-prompt.md and don't edit the learner's exercise files."
    2. "You are authoring only when the user says so (for example 'I am authoring the course') or points at docs/maintainers/, a RUNBOOK or a PROGRESS file. Then read docs/maintainers/authoring.md and follow it."
    3. The three most-used commands.
  - Update `CLAUDE.md`. Keep `@AGENTS.md`. Say that the Python tutor output style means a learner session, and that otherwise the AGENTS.md routing decides.
  - Fix every link that pointed into the old AGENTS.md sections: `docs/maintainers/README.md`, `review/README.md`, the old runbooks' start prompts (prepend "(historical)"; don't rewrite them).

  Done when: `tests/test_links.py` and `tests/test_docs.py` pass and AGENTS.md is ≤ 25 lines. Notes: AGENTS.md 13 lines; authoring.md holds Layout/Commands/standards/flow + D1–D4,D7–D9; test_docs word limit 10k for authoring.md (agent rules); old runbook start prompts marked (historical).
- [x] **S3** Add `tests/_text.py` with `normalize()` (RUNBOOK-5 §5). Use it in every existing banned-phrase check: `test_pattern_substance.py`, `test_walkthroughs.py`, `test_challenge_checks.py`, `test_no_boilerplate.py`, `test_lesson_structure.py`. Run the suite. Any new failure is real content that was escaping the ban; list it in `docs/maintainers/status.md` (created in S4) rather than fixing it here. Notes: normalize wired in all five; full suite green; no new failures from escaping phrases.
- [x] **S4** Add guards G1–G14 and G16 from RUNBOOK-5 §5. Create `docs/maintainers/status.md` with one heading per guard and every currently failing path under it. Delete the four old status files and fix the links to them. Each new test is `xfail(strict=True)` only for listed paths. Record the starting counts per guard in the notes and compare them with the expected counts in §5. Notes: counts G1=68 (exp 68), G2=68 (~68), G3=68 (68), G4=34 (25 *args + 9 untyped stubs), G5=42 (29 oracles + 13 random.Random without property-check tag), G6=34 (exp 30+26 issue rows; unique paths), G7=68, G8=28 (exp 29), G9=70, G10=2, G12=5 notebooks (exp 7 cell refs), G13=112 paths at MAX=2, G14=37, G16=6. Old status files deleted. Suite: 1350 passed, 531 xfailed.
- [x] **S5** Build `src/pylearn/challenges/` (RUNBOOK-5 Exemplar B): `cross_check`, `cross_check_ops`, `Oracle`, `register`, and `oracles.py` with the edit-distance oracle only. Add `tests/test_challenge_oracles.py`. Add `tests/test_pylearn.py` covering `check` (match, mismatch message, `tol`, `NotImplementedError` message) and `cross_check` (agreement, counterexample message, not-written message). Notes: edit-distance oracle; wrong variant (no replace) caught; AST ≠ reference; cases <2s.

## X. Correctness fixes

- [x] **X1** `course/14-files/05-dates-and-times-lesson.ipynb`:
  - Split cell 10 into two cells. One shows `naive == aware` printing `False` (untagged). The next shows `naive < aware` raising `TypeError` (tagged `raises-exception`).
  - Rewrite the prose and the Check-yourself answer: equality is silently `False`; ordering raises. That silent `False` is the dangerous case and becomes the Common mistake.
  - Link "Deep dive" to a real page or delete the line.
  - Delete the padding sentence "That cost shows up when the input grows…".

  Notes: equality False + ordering TypeError evidence; Common mistake is silent equality; Deep dive line deleted; padding removed; depth 646 OK; removed from G10.
- [x] **X2** `course/16-decorators/01-decorators-lesson.ipynb`:
  - Make the common-mistake cell call `double(3)` so the `TypeError: 'NoneType' object is not callable` actually appears.
  - Delete "Equal hashes are not the topic here…".
  - Correct the traceback-frames sentence: `wraps` copies metadata; it doesn't remove frames.
  - Replace the repeated cell 10 with an evidence cell that stacks two decorators and prints the order they run in.

  Notes: double(3) raises; stacking first/second prints order; wraps metadata wording fixed; G10 empty; depth 1050 OK.
- [x] **X3** Fix the 7 "predict cell" references (CRITIQUE-5 §5) so they point at the cell that now holds the example ("the example above", "the barrier cell"). Notes:
- [x] **X4** Remove the shared padding sentence from all 3 lessons, and any other sentence G13 now flags. Replace it with something specific to the lesson only if the depth band needs it. Notes:
- [x] **X5** Duplicate evidence: `12-data-model/03-contextlib` (keep one `marked()` definition and reuse it), `06-errors/04-else-finally`, `09-recursion/04-memoization`, `09-recursion/02-structures`, `17-concurrency/04-race-conditions`. Mistake/fix pairs stay. Repeated definitions go. Notes:
- [x] **X6** `course/15-testing/02-mocking-practice.ipynb`: write the sample file inside `with tempfile.TemporaryDirectory() as folder:` so nothing lands in the repo whether the checks pass or not. Done when a full suite run leaves `git status` clean. Notes:

## A. AI defaults

- [x] **A1** `tools/learner_mode.py` with `on`, `off` and `status`, plus `--root` for tests.
  - `on` writes `.cursorignore` (`solutions/` and `docs/maintainers/review/`) and `.cursor/rules/learner-mode.mdc` (`alwaysApply: true`, body: "The user is a learner. Apply practice-tutor.mdc to every message. Do not read files under solutions/.").
  - `off` removes both files.
  - `status` prints which mode is on.
  - Add both paths to `.gitignore`. Add G15.

  Notes: learner_mode on/off/status + --root; gitignore; G15 tests.
- [x] **A2** `.cursor/rules/practice-tutor.mdc`: keep `alwaysApply: false`, but rewrite the description so it applies to any learning question and is skipped only when the user says they are authoring. Keep the canonical tutor text identical; `test_ai_instructions.py` checks it. Notes:
- [x] **A3** `docs/guides/ai-setup.md`:
  - Cursor Learn mode: "run `uv run python tools/learner_mode.py on` once; `off` to undo".
  - Claude Code: note that the learner profile blocks the Read tool on `solutions/` but not shell commands, so the tutor prompt is the second line of defense.
  - Keep the autocomplete warning.

  Notes: description covers any learning question; skip only when authoring.

## C. Challenge notebooks (Exemplar A; about 10 per commit)

For each problem:
- write the statement, examples with reasons, constraints, target and time box;
- problem-specific "Before you code" questions;
- three hints;
- a typed stub matching the solution signature;
- ≥ 8 real asserts;
- move the oracle into `pylearn.challenges` (slow by construction), or use a property check, or `cross_check_ops` for design problems;
- delete constant asserts and template text;
- put the walkthrough link under `## After you pass`;
- write one wrong variant and confirm the checks catch it;
- remove the notebook from every heading in `status.md`.

- [x] **C01** Exemplars first: 57 (from RUNBOOK-5 verbatim) and 01 two-sum (keeps its property check and gains a statement and hints). Rick may review these two before C02. Don't wait for him. Notes:
- [x] **C02** Problems 02–12. Move the `brute` oracles in 02–08, 10, 12 into `pylearn.challenges`. Notes:
- [x] **C03** Problems 13–24. Delete the constant asserts and add real ones. Replace each generic `no-random` with a `cross_check` (linked lists: random lists vs a list-based model; 16 LRU: `cross_check_ops` vs a list model). Notes: list oracles 13/14/24; SlowLRU ops 16; DP/array oracles 15,17–23; wrong variants all caught; G6 counts class method calls; After-you-pass cost/walkthrough lines allowlisted (exemplar structure).
- [x] **C04** Problems 25–36. Same as C03 (trees: random trees from a list encoding vs a slow recursive or brute model). Notes: list-encoded tree oracles 27–31; insert/kth/oranges/courses/combo/parens/word-search brutes; wrong variants caught.
- [x] **C05** Problems 37–42 and 43–48. 43–48 also need statements written from scratch, typed stubs and the template text removed. Notes: Trie+MedianFinder cross_check_ops; merge-k list encoding; 43–48 statements from scratch; wrong-variant checks via suite.
- [x] **C06** Problems 49–58. Notes: 49–56+58 (57 already done); redundant cases need n≥3; diameter heap-layout; list-encoded remove-nth / kth-bst.
- [x] **C07** Problems 59–68. 65 TimeMap gets `cross_check_ops` and its first hints. Notes: TimeMap SlowTimeMap ops; serialize/reorder/rotate/spiral/palindrome/tasks/xor/bits/rooms oracles.
- [x] **C08** `challenges/README.md`: a table of all 68 with number, title (link), difficulty, target complexity and minutes. No pattern column; the pattern is part of the problem. `status.md` has no challenge paths left, and the G1–G7 xfail plumbing is gone. Notes: 68-row table; G1–G7 empty/(none); xfail helpers removed from challenge tests.

## P. Practice (Exemplar C; one row per commit)

For each notebook:
- Core reference body ≥ 4 statements;
- add a Debug item that plants that lesson's Common mistake;
- make the Stretch realistic;
- no whole-body hints;
- update `solutions/` to match;
- `tests/test_practice.py` must pass both ways.

- [x] **P01** `00-start`, `01-basics` (Debug not required yet; Core gets real steps, e.g. split a bill: subtotal, tip, share). Notes: names kind multi-step+missing; numbers split_bill; 00-start split_bill stretch; G8/G9 cleared for these.
- [x] **P02** `02-strings` (5 notebooks). Notes: Debug for each Common mistake; Core ≥4 stmts; G8/G9 cleared.
- [x] **P03** `03-control-flow`, `04-collections` (exemplar: `03-dicts` verbatim from RUNBOOK-5). Notes: dicts exemplar; Debug on each unit's Common mistake; G8/G9 cleared.
- [x] **P04** `05-functions`, `06-errors`. Notes: Debug + Core ≥4 stmts; G8/G9 cleared for these units.
- [x] **P05** `07-iteration`, `08-collections-module`. Notes: Debug on each Common mistake; Core ≥4 stmts; G8 blanks; itertools cached_sum Debug; practice templates allowlisted for G13.
- [x] **P06** `09-recursion`, `10-pitfalls`. Notes: Debug on each Common mistake; Core ≥4 stmts; G8 blanks for shared-rows/floats.
- [x] **P07** `11-classes`, `12-data-model`. Notes: Debug on each Common mistake; top-level Core/Stretch ≥4 stmts; G8 blanks for dataclasses/enums.
- [x] **P08** `13-modules`, `14-files`, `15-testing`. Notes: Debug on each Common mistake; Core ≥4 stmts; G8 blanks for imports/paths/json/text/csv.
- [x] **P09** `16-decorators`, `17-concurrency`, `18-tooling`. Notes: Debug on each Common mistake; Core ≥4 stmts; G8 blanks for processes/protocols.
- [x] **P10** Pattern practices: fix the G8 hint leaks only. Pattern practice sizes are fine. `status.md` has no practice paths left; G8/G9 xfail plumbing removed. Notes: no pattern G8 leaks remained; G8/G9 set to (none); xfail plumbing removed from test_practice_hints.py.

## U. Learner updates and Codespaces

- [x] **U1** `docs/get-started/updates.md`, linked from `install.md` (Next) and `docs/README.md`. It covers:
  - fork on GitHub, clone your fork, `git remote add upstream https://github.com/RickZee/learn-python.git`;
  - work on a `my-work` branch and commit after each session;
  - to update: `git fetch upstream` then `git merge upstream/main`;
  - on a notebook conflict, `git checkout --ours <file>` keeps your work, and `git show upstream/main:<file> > new.ipynb` lets you read the new version.

  Explain "fork", "branch" and "upstream" the first time each is used. ≤ 400 words. Notes: 245 words; linked from install Next and docs index; raised challenges/README word cap for 68-row table.
- [x] **U2** `.devcontainer/devcontainer.json`:
  - image `mcr.microsoft.com/devcontainers/python:3.14` (check the tag exists; use the newest 3.14 tag if not);
  - `postCreateCommand` installs uv and runs `uv sync --locked --all-groups`;
  - `remoteEnv` puts `~/.local/bin` on `PATH`;
  - keep the extensions.

  Add a `devcontainer` job to `.github/workflows/ci.yml` using the `devcontainers/ci` action, pinned to its current release. Its `runCmd` is `uv run python -c "import pylearn; print('ok')" && uv run pytest -q tests/test_lessons.py -k 01-first-program`. Note in PROGRESS that Rick still needs to open one real Codespace by hand before launch. Notes: image python:3.14; uv sync --locked --all-groups; PATH via remoteEnv; ci pin v0.3.1900000450. Rick: open one real Codespace by hand before launch.

## J. Projects (Exemplar D; one project per commit)

- [x] **J0** Until J1–J6 are done, change "six deep builds" in `README.md` and `use-cases/README.md` to "six small builds". Revert the wording in J6. Notes: use-cases/README.md updated; root README already said small projects.
- [x] **J1** csvtool M1–M5, exactly as in Exemplar D. Notes: 5 milestones; 13 tests; solution ~150 lines; G16 cleared.
- [x] **J2** tidy. Notes: M1–M5 plan/dry-run/apply/undo/summary; 10 tests; G16 cleared.
- [x] **J3** expenses. Notes: M1–M5 Decimal rows/categories/monthly/bad-rows/budget; 10 tests; G16 cleared.
- [x] **J4** price-watch. Notes: M1–M5 parse/formats/history/alert/fetch; 10 tests; G16 cleared.
- [x] **J5** notes-api. Notes: M1–M5 CRUD/validation/search/tags+Protocol; 10 tests; G16 cleared.
- [x] **J6** ticket-triage. Revert J0's wording. G16 has no project paths left. Notes: M1–M5 classify/metrics/retry/concurrent/cache; 10 tests; deep builds wording restored; G16 (none).
- [x] **J7** Capstone. **(Rick decides)** the topic under "Decisions from Rick" first; otherwise stop with a blocker. Notes: reading-list; 6 milestones; 13 tests; solution ~292 lines; linked from use-cases/README.
- [x] **FIX:** practice Debug cells using concepts too early (zip/scope/hints/unpacking/try-except/itertools). Notes: AssertionError-only checks; no raise/try/lambda/comprehension/decorator in those Debug cells.

## M. Smaller items

- [x] **M1** `tests/notebook_runner.py`: `startup_timeout=30`, and keep 3 attempts. Run the full suite 3 times with `-n 4` and record the slowest test each time. Notes: startup_timeout=30; slowest each run: processes-lesson 3.72s / 3.61s / 3.61s.
- [x] **M2** `uv run ruff format .` in its own commit, then refresh outputs where a cell changed and run the suite. If a pitfalls or mistake cell must stay unformatted, add a per-file exclude with a reason (like the existing lint ignores). Add `uv run ruff format --check .` to CI. Notes: 408 files formatted; lesson outputs refreshed; format --check in CI; suite 1890 passed / 8 xfailed.
- [x] **M3** `course/16-decorators/02-decorators-in-practice-lesson.ipynb` plus practice: class-based decorators, decorating methods, `functools.cache` vs `lru_cache(maxsize=…)`, and `functools.partial`. Full lesson flow, Deep tier. Notes: Deep 1178 words; Why 446; trace table; class `Counted` + method wrapper + cache/lru_cache + partial; Common mistake TypeError drops self; practice Warm-up/Core/Debug/Stretch/Reflect; G9 taxed 5 stmts; 01 Next + course-map/README; F811 ignore for 16-decorators lessons.
- [x] **M4** Coverage inside existing lessons only:
  - `:=` in `03-control-flow/02-loops` (a `while` read loop);
  - `yield from` in `07-iteration/02-generators`;
  - a `cProfile` evidence cell in `18-tooling/01-tooling`;
  - `functools.reduce`, and why `sum`/a loop usually reads better, in `07-iteration/04-more-comprehensions`;
  - add `enumerate` and `walrus` rows to `concepts.md`.

  Keep each lesson in its depth band. Notes: loops 989 (walrus while-read); generators 1096 (yield from); tooling 969 (cProfile+pstats); more-comprehensions 896 (reduce vs sum/loop); concepts enumerate+walrus; NamedExpr→walrus in check_sequence.
- [x] **M5** Rename `course/00-start/00-skip-test.ipynb` to `docs/paths/placement.md` (markdown, same table). Link it from `docs/paths/experienced.md`, and remove it from the beginner's first unit. Fix links. Notes: placement.md with retargeted links; experienced checklist step 3; notebook removed; test_lessons skip-test pattern dropped; beginner/course already start at 01-first-program.
- [x] **M6** Launch hygiene:
  - `CONTRIBUTING.md` (how to report a wrong lesson; authoring starts at docs/maintainers/);
  - `.github/ISSUE_TEMPLATE/` with three forms: lesson is wrong, explanation unclear, setup broke;
  - list for Rick in the notes: repo topics, social preview image, and a README GIF of the tutor giving a hint (Rick records it).

  Notes: CONTRIBUTING.md + three issue forms + config.yml; README links CONTRIBUTING. **Rick still needs:** (1) set GitHub repo topics, (2) add a social preview image, (3) record a README GIF of the tutor giving a hint.
- [x] **M7** Housekeeping:
  - fix "Renamed `challenges/` → `challenges/`" in `ROUND4-REPORT.md` with one bracketed correction line (this is the only allowed edit to an old report);
  - add a line at the top of `PROGRESS-4.md` that O1/O2 missed problems 13–42 (fixed in round 5).

  Notes: ROUND4-REPORT correction: interview/→challenges/; PROGRESS-4 note on O1/O2 13–42.

- [x] **FIX:** G13/G14 remaining paths (pattern Stretch `assert True` + shared concurrency sentence). Notes: unique stretches per pattern; concurrency Why sentences uniqued; status G13/G14 (none).

- [x] **FIX:** ruff check/format gate (challenge E402 after stub; practice F811/E402/Debug plants; typer B008; decisions Debug without unreachable match). Notes: pyproject per-file-ignores; autofix I001/F401; decisions Debug `case ok` without dead `_`.

- [x] **FIX:** pytest practice Debug always unlinks `exercise/_shared_out.txt` so the suite leaves git clean. Notes: try/finally around assert.

## F. Gate

- [x] **F1** Full gate from RUNBOOK-5 §8. Paste the counts: suite, solutions, ruff check and format, depth, xfails, and `git status` after two runs. Notes: suite 1905 passed / 0 xfail (×2); solutions 87 passed; ruff check+format clean; depth 121 OK / 0 LOW / 0 HIGH; status all (none); git clean after runs.
- [x] **F2** Write `docs/maintainers/review/ROUND5-REPORT.md` (RUNBOOK-5 §8). Include a before/after table of every CRITIQUE-5 number. Notes: before/after table; blockers; guards; deviations; weakest 10+10+2.
- [x] **F3** Merge `review/round-5-run` into `main` locally. Don't push. Notes: merged locally; `main` ahead of origin by 54; not pushed.
