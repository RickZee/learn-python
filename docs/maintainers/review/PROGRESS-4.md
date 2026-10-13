# Progress 4: substance, challenges rename, honest depth

Note (round 5): O1/O2 missed challenge problems 13–42; fixed in round 5.

Start only after runbook 3 is done. Work top to bottom. See [RUNBOOK-4.md](RUNBOOK-4.md) and [CRITIQUE-3.md](CRITIQUE-3.md).

## Blockers

(none)

## S. Structure, rename, guards

- [x] **S1** Create branch `review/round-4-run` from `main`. Notes: branch created.
- [x] **S2** Rename `challenges/` → `challenges/` and `solutions/challenges/` → `solutions/challenges/` with `git mv`. Rename docs paths in RUNBOOK-4's table the same way. Update every live reference (`AGENTS.md`, README, folder READMEs, paths, guides, glossary, tests, tools, pyproject if needed, tutor prompts only if they name the folder). Leave historical critique text that quotes old paths, or add one-line "(now `challenges/`)" where helpful. `tests/test_links.py` and the suite must pass. Notes: also renamed guides and paths; `test_challenge_checks.py` → `test_challenge_checks.py`; tutor wrappers synced.
- [x] **S3** README + glossary + section READMEs: present sections in learning order (course → internals → patterns → challenges → projects). Explain in one sentence that learners can ignore harness folders. Notes: kept materials flat at repo root (no nested `materials/`); learning order in README.
- [x] **S4** Guards (strict xfail via status files that only shrink):
  - Extend `tests/test_lesson_structure.py` (or add `tests/test_pattern_substance.py`): pattern lessons must include the 9-part headings; must not contain `Worked reading` or the filler *"so each step reuses prior work instead of restarting a nested scan"*. List unfinished patterns in `docs/maintainers/pattern-upgrade-status.md`.
  - Extend `tests/test_walkthroughs.py`: ban template phrases (`Name the pattern before coding`, `Keep an invariant that makes each step`, `Initialize the structure named`, `Neighboring notebooks`, `Enumerate combinations or scan naively until the cost is clear`). List unfinished walkthroughs in `docs/maintainers/challenge-upgrade-status.md`.
  - Extend `tests/test_challenge_checks.py` (rename file to `test_challenge_checks.py` if tidy): fail the generic `no-random` excuse *"compact brute oracle is not required"*. List pending oracle upgrades in the same challenge status file or a short section in it.
  Notes: 33 pattern xfails, 55 walkthrough xfails, 26 oracle xfails at start; min-cost already passed substance.
- [x] **S5** Delete `course/15-testing/_title_demo.txt`. Fix stale xfail comment in `tests/test_docs.py`. Notes: done.

## P. Patterns (substance)

One unit per item. Remove each finished lesson from `docs/maintainers/pattern-upgrade-status.md`. Exemplar: `patterns/13-dynamic-programming/01-min-cost-lesson.ipynb`.

- [x] **P01** hash-maps (01, 02). Notes: 3b57ed6; first_repeat / by_remainder siblings.
- [x] **P02** two-pointers (01–03). Notes: b21ffea.
- [x] **P03** sliding-window (01–02). Notes: 06e299e.
- [x] **P04** prefix-sums (01–03). Notes: 73cfcb7.
- [x] **P05** binary-search (01–02). Notes: b49348c.
- [x] **P06** stacks (01–02). Notes: 464967b.
- [x] **P07** linked-lists (01–02). Notes: 2efe995.
- [x] **P08** intervals (01). Notes: 068fe86.
- [x] **P09** heaps (01). Notes: 2b41729.
- [x] **P10** trees (01). Notes: 77c768a; `walk` later renamed `record_view` in suite FIX.
- [x] **P11** graphs (01–02). Notes: 314e93f.
- [x] **P12** backtracking (01). Notes: 1a7ed98.
- [x] **P13** dynamic-programming (02–03; 01 is exemplar — verify only). Notes: 35e1d94; 01 verified.
- [x] **P14** tries (01). Notes: 6f540a6.
- [x] **P15** design (01). Notes: b66a15b.
- [x] **P16** greedy (01). Notes: f3f5657.
- [x] **P17** union-find (01). Notes: a96b2dd.
- [x] **P18** shortest-paths (01). Notes: 3fe7a7e.
- [x] **P19** monotonic-deque (01). Notes: c3200a2; window-max substance; Deep OK; status cleared.
- [x] **P20** binary-search-on-answer (01). Notes: dc5e72b; smallest-divisor substance; Deep OK; status cleared.
- [x] **P21** matrix-traversal (01). Notes: b5b5daa; rotate substance; Deep OK; status cleared.
- [x] **P22** bits (01). Notes: e4c199b; xor-tricks substance; Deep OK; status cleared.
- [x] **P23** Pattern status empty; remove xfail plumbing for pattern substance. Notes: status empty; PENDING/xfail removed from `test_pattern_substance.py`.

## W. Challenge walkthroughs

Batches of problems. Rewrite thin `.md` walkthroughs; enrich empty/thin solution `.py` docstrings in the same batch. Remove finished ids from `docs/maintainers/challenge-upgrade-status.md`.

- [x] **W1** Problems 01–12 (spot-check strong ones; rewrite any thin). Notes: already substantive; no banned phrases.
- [x] **W2** Problems 13–24. Notes: ed8b89a.
- [x] **W3** Problems 25–36. Notes: 1b26ac3.
- [x] **W4** Problems 37–48. Notes: 4f55f31.
- [x] **W5** Problems 49–60. Notes: a8192a6.
- [x] **W6** Problems 61–68. Notes: 23a173e (65 already ok).
- [x] **W7** Walkthrough template bans enforce; no xfail left for walkthrough substance. Notes: Walkthroughs section empty; PENDING/xfail removed from `test_walkthroughs.py`; 68 passed.

## O. Oracles

- [x] **O1** Replace boilerplate `no-random` with randomized cross-checks where a slow oracle fits (edit distance, jump game, word break, and the rest that only used the generic excuse). Keep honest `no-random` with a specific reason. Notes: problems 43–68 got random cross-checks vs slow references (c25b73f).
- [x] **O2** Oracle status empty / checks green. Notes: `## Oracles` empty; PENDING/xfail removed from `test_challenge_checks.py`; 68 passed.

## T. Trim and stretches

- [x] **T1** Bring the 18 HIGH lessons back into depth band (trim prose or re-tier). `tools/depth_report.py` → 0 HIGH. Notes: 0f95a97 trimmed HIGH; f88fd94 restored 15 pattern LOWs → `120 OK, 0 LOW, 0 HIGH`.
- [x] **T2** Course practice stretch sweep: replace one-liner stretches with small situational tasks; update solutions only where needed; `tests/test_practice.py` green. Notes: 27 course stretches rewritten; matching solutions updated; test_practice 350 passed (91bd8d7).

## F. Polish and gate

- [x] **F1** Nav on `challenges/python-questions.md`; skimmable TOC / shorten `docs/guides/learning-with-ai.md` if over cap; confirm challenge path and guides. Notes: breadcrumb+Next; TOC line; guides confirmed.
- [x] **F2** Full suite, `PYLEARN_SOLUTIONS=1` on course/use-cases, ruff, depth 0 HIGH, status files empty. Paste counts. Notes: pytest 919 passed; solutions 23; ruff clean; depth 120 OK 0 LOW 0 HIGH; status files empty.
- [x] **F3** Write `ROUND4-REPORT.md`. Merge `review/round-4-run` into `main`. Notes: report written; merged to main (37302a3).
