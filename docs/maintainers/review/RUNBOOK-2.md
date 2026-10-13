# Runbook: finish round 2 without stopping

This runbook is for Cursor or Claude Code. It drives everything left in [AGENT_PLAN-2.md](AGENT_PLAN-2.md) (R2–R6) through to completion. [PROGRESS-2.md](PROGRESS-2.md) is the work list and the memory between sessions.

**Start or resume with:** (historical)

> Follow `review/RUNBOOK-2.md`. Continue from the first unchecked item in `review/PROGRESS-2.md`. Do not stop until every item is checked or you hit a blocker as defined in the runbook.

---

## 1. The loop

Repeat until every box in `PROGRESS-2.md` is checked:

1. **Pick** the first unchecked item. Read its line, the plan section it names, and the exemplar it names. Don't skip ahead or reorder.
2. **Do** the item in full. "Full" means it meets the item's *done when* line and the quality bar in section 3.
3. **Verify:**
   - `uv run python tools/refresh_outputs.py <changed notebooks>`
   - `uv run pytest -n auto`
   - `uv run ruff check .`
   - `uv run python tools/depth_report.py <changed lessons>` (once item S3 exists)

   Everything must pass. If something fails, fix it and verify again. A failing test is part of the item, not a reason to stop.
4. **Self-review** against the checklist in section 3, and write the answers into the item's notes line in `PROGRESS-2.md`. Keep it short, for example: `why: hash table + O(1) + hashable keys, evidence cell timeit; mistake: fromkeys shared list (silent)`.
5. **Commit** with a message that names the item, e.g. `R2.05: depth pass on 04-collections`. Tick the box in `PROGRESS-2.md` in the same commit.
6. **Go to step 1.** Don't ask for confirmation between items. Don't write a summary between items, because the progress file is the summary.

**Context limits.** After every 3 items, and before your context gets long, make sure `PROGRESS-2.md` is committed and accurate. If the session ends or Cursor pauses (tool-call limit, context), the next session resumes from the progress file with the start prompt above. Never redo a checked item unless a later test proves it broken. If that happens, add a `FIX:` item directly below the current one, then continue.

**Branch.** Work on one branch, `review/round-2-run`, created from `main` in item S1. Merge to `main` only in item F5.

---

## 2. When you may stop

Stop and ask only for one of these. Write the blocker into `PROGRESS-2.md` under **Blockers** before stopping.

- A needed package won't install, or the environment is broken in a way you can't fix inside the repo.
- Two instructions in the plan contradict each other, and choosing would change teaching content in a way that's hard to undo.
- A test can only pass by doing something that section 4 forbids.

Not blockers: a hard lesson, a failing test you caused, the volume of remaining work, uncertainty about wording (use the exemplars), or wanting a review (the progress notes and commits are the review).

---

## 3. Quality bar (check every item against this)

**Lessons** in `course/`, `patterns/` and `internals/`:

- [ ] **Why it works this way** explains the *mechanism*, its *cost* (time and memory), and the *design reason*. At least one code cell shows evidence (`timeit`, `sys.getsizeof`, `id`, `dis`, `__mro__`, a counter of calls). It links to the matching `internals/` lesson.
- [ ] Answers to "why" questions don't restate the fact. Test: could someone who only knew the *what* have written the answer? If yes, rewrite it.
- [ ] **When to use it** names a better alternative for at least one case.
- [ ] **Predict** targets a real misconception (aliasing, laziness, `//` with negatives, `or` with `0`, and so on), not a trivial print.
- [ ] **Common mistake** is a bug learners actually make. Silent bugs show the wrong output, then the fix and the reason.
- [ ] **Modify** requires understanding, not a one-character edit.
- [ ] The word count is in the tier's range (R0.3). It got there by adding explanation, examples and evidence, not padding or repeated phrasing.
- [ ] Every factual claim is backed by a cell that runs. CPython-only details are labelled.
- [ ] Each worked example is a complete, realistic solution. Pattern lessons follow the 9-part structure in R5 and Exemplar B.
- [ ] `**Uses:**` are links, and no concept appears before its lesson.

**Challenge problems:**

- [ ] The notebook has examples with reasons, problem-specific "Before you code" prompts, and specific follow-ups.
- [ ] At least 8 checks: examples, edge cases, a randomized cross-check against an in-notebook brute force or a definition, and a scale check where the target beats brute force.
- [ ] You wrote one deliberately wrong variant, confirmed the checks catch it, and recorded it in the item notes.
- [ ] The walkthrough `.md` has all 11 headings, is at least 350 words, and includes a trace table. Exemplar C is the bar.

---

## 4. Never do these

- Don't weaken, skip or delete a test, lower a threshold, or add `xfail`, `skip` or `noqa` to get past a check. The only `xfail`s allowed are the ones listed in `docs/upgrade-status.md`, and that list only shrinks.
- Don't delete or shorten teaching content to escape a check.
- Don't hand-write notebook outputs.
- Don't put solutions in learner-facing files.
- Don't solve a challenge problem inside `patterns/`.
- Don't edit files in `review/` other than `PROGRESS-2.md` and the final `ROUND2-REPORT.md`. This overrides the older "leave `review/` alone" rule for those two files only.
- Don't rewrite reference solutions that already pass the random cross-checks, unless an item asks for it.
- Don't add third-party packages to `course/`, `patterns/` or `internals/`.
- Don't push, open PRs, or change CI secrets.

---

## 5. The final gate (items F1–F5)

The run is done only when all of these hold:

- `docs/upgrade-status.md` lists nothing, and `tests/test_lesson_structure.py` reports **0 xfail**.
- `tools/depth_report.py` shows every lesson within its tier range.
- Every challenge problem passes `tests/test_challenge_checks.py` and `tests/test_walkthroughs.py`.
- `uv run pytest -n auto`, `PYLEARN_SOLUTIONS=1 uv run pytest -n auto course use-cases` and `uv run ruff check .` all pass on a fresh `uv sync --all-groups`.
- `review/ROUND2-REPORT.md` exists. It covers:
  - what changed, with counts
  - each blocker and how it was resolved
  - any deviations from the plan and why
  - the depth report table
  - a list of 10 lessons and 5 walkthroughs you consider the weakest, so a human can review them first
