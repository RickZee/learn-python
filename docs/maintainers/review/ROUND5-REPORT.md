# Round 5 report

## What changed

- Honest guards G1–G16 with `normalize()`, status-driven `xfail`, then zero pending paths.
- Challenge notebooks: statements, hints, typed stubs, real asserts, oracles in `pylearn.challenges` (no in-notebook brutes), walkthrough only under After you pass; 68-row README table.
- Practice: Warm-up → Core → Debug → Stretch → Reflect; Core/Stretch ≥ 4 statements; Debug plants each lesson's Common mistake; hint leaks cleared.
- Projects: six builds as milestones with per-milestone tests; capstone reading-list tool (CLI + API + SQLite + CSV + enrich).
- AI defaults: `AGENTS.md` tutor router; `authoring.md`; opt-in `learner_mode`; practice-tutor description; AI setup docs.
- Learner updates doc; Codespaces image/devcontainer CI job; notebook `startup_timeout=30`; ruff format + CI `format --check`.
- Deep `02-decorators-in-practice`; coverage for `:=`, `yield from`, `cProfile`, `reduce`; `enumerate`/`walrus` in concepts; placement quiz moved to `docs/paths/placement.md`; CONTRIBUTING + issue templates.

## Before / after (CRITIQUE-5)

| Signal | Before | After |
| --- | ---: | ---: |
| Challenge notebooks without a real statement | 68 | 0 |
| Hints only "see walkthrough" / missing | 68 | 0 |
| Notebooks with constant/padding asserts (13–42) | 30 (126 asserts) | 0 |
| Generic hyphenated `no-random` excuses | 26 | 0 |
| Untyped `*args, **kwargs` stubs (43–68 cluster) | 25 | 0 |
| In-notebook reference/oracle implementations | 29 | 0 |
| Course practices with Core ≤ 2 lines | 42 | 0 (G9 ≥ 4 stmts) |
| Practice hints that leak the full reference body | 29 | 0 |
| Project tests (six builds) | 12 | 63+ (milestones) |
| Project reference size (six builds) | ~180 lines | ~several hundred + capstone ~292 |
| Capstone | none | reading-list (6 milestones) |
| Cursor default authoring in AGENTS | yes | tutor router; authoring only when said |
| Learner update / fork doc | none | `docs/get-started/updates.md` |
| Codespaces image / locked sync / CI job | moving `python:3`, no locked | `python:3.14` + locked + CI |
| `startup_timeout` | 120 | 30 |
| Unformatted files (`ruff format --check`) | 407 | 0 |
| G13/G14 pending paths | many | (none) |
| Suite xfails | 531 (start of S4) | **0** |
| Depth LOW/HIGH | — | **0 / 0** (121 lessons) |

## Gate counts (F1)

| Check | Result |
| --- | --- |
| `uv sync --locked --all-groups` | ok |
| `pytest -n 4` (run 1) | 1905 passed, 0 xfailed |
| `pytest -n 4` (run 2) | 1905 passed, 0 xfailed |
| `PYLEARN_SOLUTIONS=1 pytest -n 4 course use-cases` | 87 passed |
| `ruff check .` | All checks passed |
| `ruff format --check .` | 805 files already formatted |
| `tools/depth_report.py` | 121 OK, 0 LOW, 0 HIGH |
| `docs/maintainers/status.md` | every guard `(none)` |
| `git status` after two suite runs | clean |

## Blockers and resolutions

- **J7 capstone topic:** Rick chose the reading-list tool (2026-10-12). Built as six milestones under `use-cases/capstone/`.

## Guards changed and why

- Added G1–G16 (and G15 learner_mode) as specified in RUNBOOK-5 §5; `normalize()` on banned-phrase checks; `MAXIMUM_NOTEBOOKS = 2`.
- Challenge oracles live in `pylearn.challenges` (D1); property checks stay in-notebook where appropriate.
- Pedagogical `per-file-ignores` for challenge stub-then-import (E402), practice cross-cell redefs (F811/E402), Debug planted mistakes, and Typer `B008` — so `ruff check` matches how notebooks are taught.
- Removed remaining G13/G14 xfails: unique concurrency Why sentences; real pattern Stretch asserts instead of `assert True`.

## Deviations

- Early merge after C–J6 was moot; merged only at F3 as planned.
- Extra FIX commits after M7 for G13/G14, ruff gate, race-conditions Why floor, and pytest Debug leftover file (suite must leave `git status` clean).
- `NamedExpr` → `walrus` wired in `check_sequence.py` when adding the concepts row (enforcement, not just documentation).
- Rick still needs by hand: real Codespace open (U2), repo topics, social preview image, README tutor-hint GIF (M6).

## Weakest for Rick to review first

**Challenges (10):** 43–48 (statements written from scratch this round), 16 LRU (`cross_check_ops`), 65 TimeMap, 57 edit-distance exemplar, 01 two-sum (property check).

**Practices (10):** `16-decorators/02-decorators-in-practice`, `03-control-flow/01-decisions` (Debug match plant), `15-testing/00-pytest` (isolation Debug), `05-functions/03-scope`, `06-errors/01-try-except`, `12-data-model/01-dunder`, `17-concurrency/04-race-conditions`, `04-collections/03-dicts` (exemplar), `07-iteration/02-generators`, `18-tooling/01-tooling` (if practiced via tooling unit).

**Projects (2):** `use-cases/capstone` (reading-list), `use-cases/04-services` (notes-api Protocol/tags).
