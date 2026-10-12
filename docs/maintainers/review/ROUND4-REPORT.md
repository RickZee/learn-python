# Round 4 report

## What changed

- Renamed `challenges/` → `challenges/` (and `solutions/challenges/` → `solutions/challenges/`), with learner docs, paths, and guides updated to **Challenges**. Kept materials flat at the repo root in learning order (course → internals → patterns → challenges → projects); did not nest under `materials/`.
- Substance guards: `tests/test_pattern_substance.py`, walkthrough template bans, generic `no-random` ban; status files that only shrink.
- All 34 pattern lessons restored to the 9-part body with real Why/When/Common mistake; Worked reading padding removed.
- All 68 challenge walkthroughs substantive; randomized oracles on problems that used the generic excuse.
- Depth: 0 HIGH and 0 LOW after trim + restore. 27 thin course practice stretches replaced with situational tasks.
- Polish: `challenges/python-questions.md` nav; learning-with-ai TOC; suite cleanups (why floors, `walk`→`record_view`, boilerplate, ruff).

## Counts at F2

| Check | Result |
| --- | --- |
| `pytest -n auto` | 919 passed |
| `PYLEARN_SOLUTIONS=1 pytest -n auto course use-cases` | 23 passed |
| `ruff check .` | All checks passed |
| `tools/depth_report.py` | 120 lessons, 0 LOW, 0 HIGH |
| Pattern substance | 34 passed |
| Walkthroughs + challenge checks | 68 + 68 passed |

## Structure decision (locked)

Do not nest learner materials under `materials/`. Newcomers follow the README and paths; nesting would rewrite every link and solutions mirror for little gain. Setup stays in `docs/get-started/` and `.devcontainer/`. Harness folders stay at the root and are called out as ignorable.

## Deviations

- Parallel agents raced on status files; cleaned up with a follow-up FIX commit for suite failures.
- T1 briefly produced 15 pattern LOWs; restored in `f88fd94`.
- W1 skipped: problems 01–12 already free of banned phrases.

## Remaining (not blockers)

- Codespaces / Windows install still not built/run on those platforms (same as DOCS-REPORT).
- More challenge staples (word ladder, N-Queens, …) can wait for a later round.
- Explore pages under `use-cases/` remain thin by design.
