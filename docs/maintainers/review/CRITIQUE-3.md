# Review, round 3: quality after the structure passes

Reviewed 2026-10-11 on `main` after rounds 1–2 (depth, internals, challenges breadth) and the runbook-3 docs/flow pass. Companion plans from earlier rounds: [CRITIQUE.md](CRITIQUE.md), [CRITIQUE-2.md](CRITIQUE-2.md), [PROGRESS-2.md](PROGRESS-2.md), [PROGRESS-3.md](PROGRESS-3.md).

## Verdict

The repo now looks finished from the outside. Setup works, CI is green (~885 tests), every lesson has the teach-first shape, every practice has warm-up → core → stretch → reflect, docs navigate from the README, and `tools/depth_report.py` shows **0 LOW**. Course and internals lessons largely teach mechanism and cost. That is real progress.

What remains is **content that passes the harness without teaching**. Most pattern lessons pad Why / When / Common mistake and invent "Worked reading" cells so word counts clear. Many challenge walkthroughs hit 350 words and eleven headings with template sentences. Fifty-two of sixty-eight problems use a boilerplate `no-random` excuse instead of a cheap oracle. Eighteen lessons sit **HIGH** on depth after flow cells were added. The next round should raise the bar for substance, not add more surface area.

## Goals (what this repo is for)

From `README.md` and `AGENTS.md`: a free, notebook-first path that teaches idiomatic Python, how it works underneath, algorithm patterns, and small projects — with an AI tutor that explains while the learner writes the code.

| Audience | Promise |
| --- | --- |
| Beginners | A clear course order, checkable practice, get-started docs |
| People who know another language | Internals + idioms, not a slow hello-world crawl |
| Challenge prep | Patterns, 68 problems with walkthroughs, Python question bank |
| Builders | Six projects plus explore pages |

Rounds 1–3 delivered the skeleton and most of the course/internals depth. Round 4 should make every learner-facing page earn its word count.

## How I checked

- Ran `tools/depth_report.py`: **120 lessons, 102 OK, 0 LOW, 18 HIGH**.
- Collected the suite: **885 tests**.
- Grepped pattern lessons for shared filler and padding cells.
- Sampled Why / When / Common mistake in course, internals, and patterns.
- Sampled challenge walkthroughs (strong vs templated) and counted `random` vs `no-random`.
- Checked practice headings repo-wide, use-case layout, and docs hard pages from [DOCS-REPORT.md](DOCS-REPORT.md).

## What improved since round 2

- Teach-first lesson flow everywhere; `docs/maintainers/flow-upgrade-status.md` is empty.
- Newcomer docs: get-started, paths, folder READMEs, Codespaces `.devcontainer`, `tests/test_docs.py` green.
- Recursion unit, twelve internals lessons, forty-eight Python questions, patterns 16–22, challenge problems 43–68, second codebase round.
- Course and internals Why / When sections are usually mechanism + cost + design, with silent common mistakes where they belong.
- Link, structure, walkthrough-heading, and challenge-check tests enforce shape.

## 1. Patterns: green tests, hollow prose (highest severity)

**Evidence**

| Signal | Count |
| --- | --- |
| Shared Why filler: *"so each step reuses prior work instead of restarting a nested scan"* | **26 / 34** lessons |
| Fake `## Worked reading N for …` cells (no code, slug soup) | **33 / 34** |
| Contrived Common mistake (`print({}[1])` / "mistake demo") | **24 / 34** |

Example from `patterns/01-hash-maps/01-first-unique-lesson.ipynb`:

> The 01 hash maps lesson 01-first-unique-lesson keeps hash map buffers so each step reuses prior work instead of restarting a nested scan for 01 first unique lesson.

That is not teaching. It is a word-count patch. `patterns/13-dynamic-programming/01-min-cost-lesson.ipynb` still looks like a real pattern lesson (recurrence, silent DP off-by-one). Use it as the bar.

`AGENTS.md` still requires the 9-part pattern body (Recognize it through Python idioms). The flow test only requires the first cell plus Quick review for patterns, so padding can sit next to a real Recognize/Brute-force body and still pass.

**Fix:** rewrite Why / When / Common mistake per lesson for the sibling problem; delete every Worked reading cell; restore a real silent or realistic mistake; extend `tests/test_lesson_structure.py` to require the 9-part headings and to fail on `Worked reading` and on the shared filler phrase.

## 2. Challenge walkthroughs: headings without algorithms

**Evidence**

- **68** problems, each with a `.md` walkthrough that clears ≥350 words and the required headings.
- Strong examples still exist: `01-two-sum.md`, `02-group-anagrams.md`, `07-merge-intervals.md`, `09-binary-search.md`.
- Thin examples: `16-lru-cache.md`, `41-minimum-window-substring.md`, `57-edit-distance.md` — phrases like "Name the pattern before coding", "Keep an invariant…", "Initialize the structure named…", "Neighboring notebooks…".
- Template markers appear across a large majority of walkthroughs (especially 13+ and many of 43–68).

A stuck learner who opens the walkthrough for Edit Distance or LRU Cache does not get a trace table, a failed greedy or wrong recurrence, or a complexity derivation. They get a filled template.

**Fix:** rewrite thin walkthroughs to Exemplar C substance (concrete recognize signals, brute force with a cost argument, key insight in one sentence about *this* problem, numbered algorithm steps that mention real structures, a filled trace, complexity with *why*, alternatives, common bugs that match the planted wrong variants). Ban the template phrases in `tests/test_walkthroughs.py`.

## 3. Challenge checks: `no-random` as a dodge

| Tag | Count |
| --- | --- |
| Uses `random` (or a real randomized cross-check) | **16** |
| Uses `no-random` | **52** |

Many `no-random` notes say a compact brute oracle is "not required for this round." That satisfied round-2 item R6.3; it does not protect learners. Edit Distance, Jump Game, Word Break, and similar problems have cheap oracles.

**Fix:** for each `no-random` problem, either add a randomized cross-check against a slow correct reference, or keep `no-random` only with a specific reason (nondeterministic concurrency, interactive design API, etc.). Tighten `tests/test_challenge_checks.py` so the generic excuse fails.

## 4. Depth HIGH after flow (18 lessons)

Flow cells (Quick review, Check yourself) pushed many Core lessons over 600 words and a few Deep internals over 1600.

| Band | Paths (examples) |
| --- | --- |
| Core HIGH | `course/00-start/*`, `01-basics/*`, `02-strings/*`, `04-collections/{01,02,05}-*` |
| Deep HIGH | `internals/02-mutability`, `03-lists`, `04-dicts`, `06-scopes`, `12-gil` |

PROGRESS-3 accepted the 18 HIGH. That was pragmatic for the flow merge; it should not stay permanent.

**Fix:** trim prose (not evidence cells), or re-tier a few Core lessons to Intermediate if the topic truly needs the space. Target **0 HIGH** again, or raise the Core ceiling in the tool and document why.

## 5. Practice stretches: present, sometimes tiny

Every practice has Warm-up / Core / Stretch / Reflect. Some stretches are realistic (async `first_done`, dict store APIs). Others are one-line skill checks ("yield evens", "decorator adds 1").

**Fix:** sweep course practices whose stretch is a one-liner; replace with a small situational task that still uses only taught concepts. Keep pattern stretches as variants of the sibling problem.

## 6. Coverage and product polish (lower severity)

Still worth doing, but after the hollow-content fixes:

| Gap | Why it matters |
| --- | --- |
| Challenge staples still missing (longest consecutive, word ladder, tree construct / max path, alien dictionary, gas station, N-Queens, …) | Prep lists learners compare against |
| Empty/thin solution `.py` docstrings on some problems | Opening the `.py` alone should still teach |
| `challenges/python-questions.md` has no breadcrumb / Next | Feels like a doc island |
| `docs/guides/learning-with-ai.md` is long (~900+ words) | Easy to miss the one rule |
| Explore pages vs six projects | Easy to open too many thin field pages |
| `.devcontainer` and Windows install untested | DOCS-REPORT still lists them |
| Untracked junk `course/15-testing/_title_demo.txt` | Noise |
| Stale "xfail until D16" comment in `tests/test_docs.py` | Harness hygiene |
| `docs/maintainers/concepts.md` maps `decorators` to dataclasses | Confusing for humans; harness-only map |

## What not to do next

- Do **not** add another large batch of problems or explore pages until patterns and walkthroughs are substantive.
- Do **not** pad word counts. If a section is short and true, keep it short; if the harness requires length, the harness is wrong.
- Do **not** reopen the lesson-flow order. Flow is done; this round is substance.

## Fix order (round 4)

1. **Guards first.** Ban `Worked reading`, the shared pattern Why filler, and the walkthrough template phrases. Fail generic `no-random` excuses. Optionally fail Core HIGH above a new ceiling. Put pending lessons/problems in a status file that only shrinks (same pattern as rounds 2–3).
2. **Patterns rewrite** (one unit per commit): Why / When / Common mistake + delete padding; keep a real 9-part body and a complete sibling solution. Start from hash-maps through bits; use min-cost as the exemplar.
3. **Challenge walkthroughs** in batches of ~10: rewrite thin `.md` files; enrich empty solution docstrings in the same pass.
4. **Random oracles** for problems where a brute reference is easy; keep honest `no-random` only where needed.
5. **Depth trim** on the 18 HIGH lessons; practice stretch sweep on thin course practices.
6. **Polish:** delete `_title_demo.txt`, fix test docstring, nav on `python-questions.md`, skimmable TOC for learning-with-ai, validate Codespaces once, then optionally add a small set of high-ROI challenge problems.
7. **Final gate:** full suite, solutions run, ruff, depth 0 HIGH (or documented new band), status files empty, short `ROUND4-REPORT.md`.

## Suggested agent kickoff

> Read `docs/maintainers/review/CRITIQUE-3.md`. Do **phase N** only (guards → patterns → walkthroughs → oracles → trim → polish → gate). Follow `AGENTS.md`. Never pad. Never type notebook outputs; use `tools/refresh_outputs.py`. When done, show acceptance checks and stop.

## Success looks like

A learner can open any pattern lesson and get a real why, a real mistake, and a full sibling solution — with no slug soup. A learner stuck on Edit Distance or LRU opens a walkthrough that traces the table. Random checks catch half-right solutions on problems that admit oracles. Depth is honest again. The suite still passes.
