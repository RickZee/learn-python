# Runbook 4: substance, rename, and honest depth

Run this after runbook 3 (`PROGRESS-3.md` D19). Work list: [PROGRESS-4.md](PROGRESS-4.md). Reasons: [CRITIQUE-3.md](CRITIQUE-3.md).

**Start or resume with:**

> Follow `docs/maintainers/review/RUNBOOK-4.md`. Continue from the first unchecked item in `docs/maintainers/review/PROGRESS-4.md`. Do not stop until every item is checked or you hit a blocker as defined in `RUNBOOK-2.md`.

Same loop as RUNBOOK-2: pick → do → verify → self-review notes → commit → next. Branch: `review/round-4-run`. Never pad word counts. Never type notebook outputs; use `tools/refresh_outputs.py`.

---

## Structure decisions (locked)

### Keep materials at the repo root (do not nest under `materials/`)

Learners follow the README and paths, not `ls`. Nesting `course/`, `internals/`, `patterns/`, `challenges/`, and `use-cases/` under one parent would rewrite every link, every solutions mirror path, and every Codespaces/get-started instruction for little gain. Root already tells newcomers to ignore `src/`, `tests/`, and `tools/`.

### Order sections by learning path (in docs, not by renaming numbers)

In README and folder READMEs, present sections in this order:

1. `course/` — language
2. `internals/` — how Python works (open when a course lesson links it)
3. `patterns/` — algorithm patterns on sibling problems
4. `challenges/` — timed problems, codebase rounds, Python questions (was `challenges/`)
5. `use-cases/` — projects and explore pages (folder name stays; learner word is *project*)

Setup stays under `docs/get-started/` and `.devcontainer/`. Maintainer and harness stay at the root (`src/`, `tests/`, `tools/`, `solutions/`, `docs/maintainers/`).

### Rename the challenges section (historical)

Do not publish a top-level folder under any former section name. Learner-facing section name: **Challenges**. Paths that moved into the Challenges branding:

| Role | Canonical path |
| --- | --- |
| Top-level section | `challenges/` |
| Solutions mirror | `solutions/challenges/` |
| Path doc | `docs/paths/challenges.md` |
| Practice guide | `docs/guides/challenge-practice.md` |
| Timed-session guide | `docs/guides/timed-session.md` |
| Upgrade status | `docs/maintainers/challenge-upgrade-status.md` |

Audience path "preparing for timed challenges" may still exist as *who it's for*, but every link and heading for the section says Challenges. In learner text prefer *problem*, *challenge*, *timed practice*.

Update all live learner and maintainer entry points to those paths. Do not leave the old section name in headings, links, or copy.

---

## Phase overview

| Phase | Goal |
| --- | --- |
| **S** | Branch, rename, structure docs, anti-padding guards + status files |
| **P** | Rewrite hollow pattern Why/When/CM; delete Worked reading |
| **W** | Rewrite thin challenge walkthroughs + solution docstrings |
| **O** | Real randomized oracles where cheap; honest `no-random` only |
| **T** | Trim 18 HIGH lessons; thicken thin course practice stretches |
| **F** | Polish, empty status files, full gate, ROUND4-REPORT, merge |

---

## Quality bar

**Patterns.** Why explains mechanism/cost/design for *this* sibling problem. Common mistake is a real silent or realistic bug for the pattern (not `print({}[1])`). No `Worked reading` cells. No shared filler phrase from CRITIQUE-3. Nine-part body intact.

**Walkthroughs.** Concrete recognize signals, brute force with cost, key insight about *this* problem, algorithm steps naming real structures, a filled trace, complexity with why, alternatives, common bugs. Ban template phrases listed in PROGRESS-4 S4.

**Oracles.** Prefer random cross-check vs slow correct reference. `no-random` only with a specific technical reason (design API surface, nondeterminism, etc.), never "not required for this round".

**Depth.** Target 0 HIGH from `tools/depth_report.py`, or document a raised Core ceiling in the same commit that changes the tool.
