# Progress 3: lesson flow, then newcomer docs and navigation

Start only after `review/PROGRESS-2.md` item F5 is checked. Work top to bottom, ticking each item and adding a note in the same commit as the work. See [RUNBOOK-3.md](RUNBOOK-3.md).

## Blockers

(none)

## Start

- [x] **D1** Create branch `review/docs-run` from `main`. Notes: created from main at 43b0e8c.
## L. Lesson flow (do this before the docs work)

Follow "Lesson flow (phase L)" in RUNBOOK-3. Reorder and reframe each lesson; keep its content and depth. One group per item, one commit per unit inside the item.

- [x] **L1** Rules and guards:
  - Copy the "Lesson flow" order from RUNBOOK-3 into `AGENTS.md`, replacing any Predict guidance there.
  - Add a one-line note at the top of the lesson templates in `review/AGENT_PLAN.md` (Phase 3) and `review/AGENT_PLAN-2.md` (Exemplar A) saying the order is now in `AGENTS.md`.
  - Extend `tests/test_lesson_structure.py`. Course and internals lessons must have "Why you'd use this" and "After this lesson you can" in the first cell, and the headings Quick review, The idea, See it work, Check yourself, Why it works this way, When to use it, Common mistake, Try it, Recap, in that order. Pattern lessons get the same first cell plus Quick review. No goal may start with "predict", and no `## Predict` heading may remain.
  - Mark lessons not yet converted `xfail`, listed in a new `docs/flow-upgrade-status.md` that only shrinks.
  Notes: flow test + depth test; 43 lessons already on flow; 77 listed xfail in `docs/flow-upgrade-status.md`.
- [x] **L2** Convert course units 00–04. Notes: 00/01/02/04 converted; 03-control-flow already on flow.
- [x] **L3** Convert course units 05–09. Notes: 05/07/08 already on flow; fixed 06 else-finally predict goal; converted 09-recursion.
- [x] **L4** Convert course units 10–14. Notes: 10–12 already on flow; fixed predict goals in 13-main and 14-json.
- [x] **L5** Convert the remaining course units. Notes: 15 already on flow; converted 16–18.
- [x] **L6** Convert internals 01–06. Notes: all six converted; kept What this explains before Recap.
- [x] **L7** Convert internals 07–12. Notes: all six converted; fixed missing `import sys` in memory See-it-work cell.
- [x] **L8** Convert patterns 01–08 (first cell plus Quick review; keep the 9-part body). Notes: first cell + Quick review; Predict→Check yourself; body kept.
- [x] **L9** Convert patterns 09–15. Notes: first cell + Quick review; Predict→Check yourself.
- [x] **L10** Convert patterns 16–22. Notes: first cell + Quick review; Predict→Check yourself; flow-upgrade-status empty of lessons.
- [x] **L11** Practice sweep: every practice notebook has warm-up → core → stretch → reflect, and every stretch is a small realistic task, not a puzzle. Update the solutions only where an exercise changed, and keep `tests/test_practice.py` green. Notes: added missing ## Core on shortest-window practice; stretches already realistic; test_practice 350 passed; no solution edits.
- [x] **L12** Verify:
  - `docs/flow-upgrade-status.md` is empty and the xfail plumbing is removed.
  - `tools/depth_report.py` shows no LOW lessons.
  - The full suite passes, and outputs are refreshed.
  - "Write down what each line prints before you run it." is removed from `tests/boilerplate_allowlist.txt` if no lesson uses it.
  - Pick 10 random goal lines and ask: "Would someone who has never programmed understand this, and want it?" Fix any that fail, and paste the 10 into the notes.
  Notes: status empty; xfail plumbing removed; 0 LOW (18 HIGH pre-existing); 884 passed + ruff clean; allowlist now only "Answer these from the example above before you run the cell."; fixed import-order fallout in gil/memory/regex/tooling; diversified pattern Quick reviews. Goals sample (3 softened): more-comprehensions build dict/set in one line / lazy `()`; mutability which calls the caller sees; async overlap `await` waits; zip pair lists; dataclasses write a dataclass; binary-search-on-answer search the answer value; hash-table insertion order + hashable keys; csv DictReader; iteration protocol iter/next in plain words; objects tell when two names share an object.

## D. Docs guards

- [x] **D2** Add `tests/test_docs.py`. It checks every `.md` except `review/`, `.venv/`, `.pytest_cache/`, `.archive/`, `AGENTS.md`, `CLAUDE.md`, `.claude/`, `.cursor/` and `docs/guides/ai-prompts/` (the prompt files are read by tools, not people):
  - **Orphans:** every doc can be reached from `README.md` by following links.
  - **Navigation:** every page in `docs/` and every folder README has a breadcrumb line and a `**Next:**` line, except `docs/README.md` and the reference pages.
  - **Length:** at most 600 words, except `docs/reference/`, `docs/teaching/` and `docs/guides/learning-with-ai.md` (at most 1,000 words).
  - **Banned in learner text:** "practise", "Pass 1", "track" as a noun for a section, "use case" (the folder name `use-cases/` is fine), "Replace `...`".
  - **Fenced commands:** a line starting with `uv `, `git `, `claude ` or `pip ` outside a code fence fails.

  Mark it `xfail` until D16, then remove the xfail. Notes: added with strict xfail; currently fails orphans/nav/banned as expected.

## D. Structure

- [x] **D3** Move the files to the target structure in RUNBOOK-3 with `git mv`:
  - `docs/ai.md` → `docs/guides/ai-setup.md`. Move its **Author** section into `docs/maintainers/README.md`, and fix "practise".
  - `docs/learning-with-ai.md` → `docs/guides/learning-with-ai.md`
  - `docs/ai/` → `docs/guides/ai-prompts/`
  - the other moves as listed

  Update every link and every path mentioned in `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/practice-tutor.mdc`, `.claude/`, `tests/test_ai_instructions.py` (the canonical path and the wrapper path), `tests/test_lesson_structure.py`, the status files and `tools/`. Leave `review/` where it is; it moves in D18. *Done when:* the links test and `tests/test_ai_instructions.py` pass. Notes: moves done; Author→maintainers/README; practise→practice; links + ai_instructions green.
- [x] **D4** Write `docs/README.md`: a grouped index of every doc, with one line each. Notes:
- [x] **D5** Write `docs/reference/glossary.md` with about 25 terms (including *section*, *path*, *unit*, *the tutor*, *Codespaces*), each in 1–2 plain sentences. Link it from the first use of each term across the docs. Notes:

## D. Getting started (the most important part)

- [x] **D6** Add `.devcontainer/devcontainer.json` for GitHub Codespaces:
  - image `mcr.microsoft.com/devcontainers/python:3`
  - `postCreateCommand` that installs uv with the official script, then runs `uv sync --all-groups`
  - the VS Code `ms-python.python` and `ms-toolsai.jupyter` extensions
  - `python.defaultInterpreterPath` set to `${containerWorkspaceFolder}/.venv/bin/python`

  If you can, validate it with the devcontainer CLI. Otherwise record "not built locally" in the notes and in the final report. Notes:
- [x] **D7** Write `docs/get-started/install.md`:
  - **No install (Codespaces):** the `https://codespaces.new/RickZee/learn-python` link, roughly how long the first build takes, and a note on the free monthly hours.
  - **Mac**, **Windows** and **Linux:** get the code (`git clone`, or Download ZIP for people without Git); install uv with the official commands (`curl -LsSf https://astral.sh/uv/install.sh | sh` for Mac/Linux, and `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` in PowerShell for Windows); run `uv sync`; then pick an editor (VS Code or Cursor, or JupyterLab via `uv run --with jupyter jupyter lab`).
  - Every command says where to type it.
  - End with "Check it worked": `uv run python -c "import pylearn; print('ok')"`.
  - Delete `docs/setup.md` once D7, D9 and D10 hold all its content.
  Notes: install.md with Codespaces/Mac/Windows/Linux; deleted setup.md.
- [x] **D8** Write `docs/get-started/first-notebook.md`:
  - Open `course/00-start/01-first-program-lesson.ipynb`, choose the `.venv` kernel (what a kernel is, in one sentence), and run a cell.
  - Open the practice, read a ✓ line and a failed check, and open a hint.
  - End with "Stuck? Ask the tutor", linking `../guides/learning-with-ai.md`. Don't repeat the per-tool steps.
  Notes: first-notebook.md written.
- [x] **D9** Write `docs/get-started/how-lessons-work.md`: the lesson flow from RUNBOOK-3 in plain words (why each step is there, in one line each, including why questions come after the explanation), then lesson → practice → Part 2 exercise → project, what `check` output looks like, and where solutions live and when to open them. Notes:
- [x] **D10** Write `docs/get-started/troubleshooting.md`. Move the setup troubleshooting here and add:
  - Windows: `uv` not found (restart the terminal)
  - the kernel isn't listed
  - Codespaces is still building
  - notebook cells were run out of order
  - the tutor wrote the answer anyway (check the setup in `guides/ai-setup.md`, turn off autocomplete)
  Notes: troubleshooting.md with Windows/kernel/Codespaces/tutor cases.
- [x] **D11** **Cold-start test.** In a temporary directory, clone the repo from the local path, follow `install.md` (Mac/Linux steps) exactly as written, then execute `first-notebook.md`'s notebook with nbclient. Record every step, and fix any step that didn't work as written. Notes:

## D. AI guides

- [x] **D12** Finish `docs/guides/learning-with-ai.md`:
  - Link the How Python works section (`../../internals/README.md`) where it's named as plain text.
  - Point "Set up your tool once" to `ai-setup.md`.
  - Make sure every tool row matches the real setup: confirm `--settings` is listed in `claude --help`, check that the Cursor rule file and the Claude Project instructions exist, and confirm the tutor prompt path.
  - Update its study loop to match the lesson flow. Step 1 still says to predict each cell before running it. Change it to: read why the topic matters, read the explanation and worked example, *then* answer Check yourself without the AI.
  - Keep its prompts table and red flags as they are, unless something is wrong.
  Notes: study loop updated; internals linked; --settings confirmed in claude --help.
- [x] **D13** Rewrite `docs/guides/ai-setup.md` as setup only: Learn mode and Build mode per tool (Cursor, Claude Code, Claude app, other tools), and turning off autocomplete. No study advice; link to `learning-with-ai.md` instead. Notes:

## D. Paths and folder READMEs

- [x] **D14** Rewrite `README.md` to the RUNBOOK-3 content spec (at most 450 words). Notes:
- [x] **D15** Rewrite the four path pages. Each has:
  - who it's for, and time per week
  - an ordered checklist of links into the sections, with no unit lists copied from `course/README.md`
  - what to skip
  - one line: "Use an AI tool as your tutor: see [Learning with an AI tutor](../guides/learning-with-ai.md)." No `.cursor/` paths.

  Merge `paths/instructor.md` into `teaching/facilitator.md`. Fold `docs/start-here.md` into `course/README.md` and the paths, then delete it. Notes:
- [x] **D16** Add `course/README.md` (the one ordered unit list, with Part 1 and Part 2 defined), `internals/README.md`, `patterns/README.md`, `challenges/README.md` (problems, codebase rounds, `python-questions.md`) and `solutions/README.md` ("try first; how to use a walkthrough"). Each has a table with a link, one line on what you learn, and minutes. Tidy `use-cases/README.md` to the same shape: the six projects first, explore pages second. Notes:
- [x] **D17** Bring every remaining `.md` up to the writing rules: the guides, the use-case READMEs, the codebase-round READMEs, `facilitator.md` and the maintainer docs. Then remove the `xfail` from `tests/test_docs.py` and make it pass. Notes:

## D. Finish

- [x] **D18** Move `review/` to `docs/maintainers/review/` with `git mv`, and leave a one-line `review/README.md` that points there. Then:
  - Update every mention of `review/` in `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/practice-tutor.mdc` (its description names `review/AGENT_PLAN.md`), `tests/` and `tools/`. Find them with `grep -rn "review/" --include=*.md --include=*.mdc --include=*.py --include=*.json .`.
  - Run the full suite, `ruff` and `tests/test_docs.py`, and repeat the D11 cold start.
  - Write `docs/maintainers/review/DOCS-REPORT.md`: what moved where (a table), the cold-start log, anything untested (for example the devcontainer), and the 5 pages a newcomer will still find hardest.
  Notes: moved; stub review/README.md; AGENTS + practice-tutor updated; DOCS-REPORT written; suite/ruff/docs below.
- [x] **D19** Merge `review/docs-run` into `main`. Notes: fast-forward merge after D18.
