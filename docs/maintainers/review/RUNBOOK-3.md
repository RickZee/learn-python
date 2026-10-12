# Runbook 3: teach first, then make the repo easy for a newcomer

Run this **after round 2 is finished** (`review/PROGRESS-2.md` item F5 checked). It uses the same loop and stop rules as [RUNBOOK-2.md](RUNBOOK-2.md): pick the next item, do it, verify, self-review, commit, tick, continue. The work list is [PROGRESS-3.md](PROGRESS-3.md). Work on a new branch, `review/docs-run`, and merge to `main` at the end.

**Start or resume with:**

> Follow `review/RUNBOOK-3.md`. Continue from the first unchecked item in `review/PROGRESS-3.md`. Do not stop until every item is checked or you hit a blocker as defined in `review/RUNBOOK-2.md`.

**Overrides for this run.** RUNBOOK-2's "never do" list applies, with two exceptions:
- You may edit `review/PROGRESS-3.md`, and add the one-line notes to `review/AGENT_PLAN.md` and `review/AGENT_PLAN-2.md` that item L1 asks for.
- You may move the whole `review/` folder in item D18.

Phase **L** (lesson flow) changes lesson notebooks, practice notebooks, `AGENTS.md`, the plan templates and the lesson tests, as listed in PROGRESS-3. Phase **D** is about docs, navigation and setup only. Neither phase changes reference solutions.

---

## Who you're writing for

Picture someone who has never used a terminal, doesn't know what Git, a virtual environment or a notebook kernel is, and found this repo through a LinkedIn post. They should be able to:

1. understand in 30 seconds what the repo is and whether it's for them
2. get to a running first notebook in 15 minutes, with no install at all if they prefer (Codespaces)
3. always know where they are and what to open next
4. know how to use an AI tool to learn without letting it do the work
5. see in every lesson why the topic matters to them before being asked any question

## Lesson flow (phase L)

**Why the change.** Round 2 built lessons around "Predict": guess the output before you're taught anything. Nearly every lesson's goals start with "predict" ("predict a queue"), which tells a newcomer nothing about what they'll be able to do. The evidence points the other way:
- Adults need to know *why* before they engage, and learn around problems they care about (Knowles).
- Novices learn best from explanation and worked examples *before* solving on their own (worked-example and expertise-reversal research).
- Questions work best as retrieval *after* teaching, spaced over time. Dunlosky et al. (2013) rate practice testing and distributed practice "high utility".
- Guessing before any teaching has small, contested benefits, and starting with failure can sap motivation.

Predicting what code does is still a useful skill. It moves to *after* the explanation, as a check most learners should pass.

**The order.** Every course and internals lesson follows it:
1. **First cell.** Title and tier, then:
   - **Why you'd use this:** a real situation in 2–4 plain sentences ("You're reading orders as they come in and must handle them oldest first…").
   - **After this lesson you can:** 2–3 plain-language goals tied to that situation. Never start a goal with "predict". Bad: "predict a queue". Good: "handle tasks in the order they arrived, like a line at a store, using a `deque`."
   - Time, and **Uses:** links.
2. `## Quick review`: 2–3 short questions on *earlier* lessons (spaced retrieval), answers in `<details>`. Omit only in the first lesson of the course.
3. `## The idea`: the explanation, with a concrete analogy, plus the existing "Explain more" layer.
4. `## See it work`: the worked example solving the situation from cell 1, with labelled steps.
5. `## Check yourself`: 2–4 quick questions on code like the example ("what does this print?", "which line is wrong?"), answers in `<details><summary>Check your answers</summary>`. They come after teaching, so most learners should get most of them right. This replaces "Predict".
6. `## Why it works this way` and `## When to use it` (unchanged).
7. `## Common mistake` (unchanged rule: a real mistake).
8. `## Try it`: change the example to do something new (was "Modify").
9. `## Recap`, then `**Next:**` the practice.

**Practice notebooks:** warm-up (Parsons or fill-in) → core → stretch → one reflect question. The stretch is a small realistic task, not a puzzle.

**Pattern lessons** keep their 9-part structure from AGENT_PLAN-2 R5, with the same first cell (why you'd use it, plain goals) and a `## Quick review` before "Recognize it".

**Keep:** the existing content of "Why it works this way", "When to use it", "Common mistake", the evidence cells and the depth targets. This phase reorders and reframes; it does not shorten.

## What's wrong today

- **README** starts with jargon ("idiomatic", "tracks", "use cases") and has no one-sentence description. It offers six entry points (Setup, Path, Language, Challenges, Use cases, paths/*), and its "Order" list duplicates `docs/start-here.md`.
- **Setup** (`docs/setup.md`) assumes Git, a terminal, uv and Cursor. It has no Windows steps, no option without installing anything, and it never says where to type commands. "Kernel" is unexplained. It still says "Replace `...`" when stubs now use `raise NotImplementedError` (also in `docs/guides/challenge-practice.md`).
- **Too many overlapping starting pages:** README, `docs/start-here.md`, `docs/language.md` and five `docs/paths/*` pages each list an order to follow.
- **AI docs overlap and mix audiences:**
  - `docs/learning-with-ai.md` is the learner guide: the rule "the AI explains, you write the code", the study loop, prompts and red flags.
  - `docs/ai.md` repeats the per-tool setup, says "practise", and has an **Author** section meant for maintainers.
  - `docs/paths/beginner.md` sends learners to `.cursor/rules/...` and doesn't mention Claude.
  - `learning-with-ai.md` names `internals/` as plain text, because that folder didn't exist yet when it was written.
- **Vocabulary drifts.** "Track", "Pass 1", "Part 1", "Path", "field" and "Language map" are used for overlapping ideas, and British and American spellings are mixed.
- **Docs are flat and mixed.** Learner pages sit next to maintainer files (`concepts.md`, `upgrade-status.md`, `challenge-upgrade-status.md`). The 2,800-word facilitator guide sits beside 70-word path pages.
- **Folders have no READMEs.** `course/`, `patterns/`, `challenges/` and `internals/` show a bare file list on GitHub.
- **The repo root is cluttered for a learner:** `src`, `tests`, `tools`, `solutions`, `review` and dotfiles, with no explanation of which to ignore.

## Target structure

```
README.md                        one page: what, who, 3-step start, map
docs/
  README.md                      index of every doc
  get-started/
    install.md                   Codespaces (no install) | Mac | Windows | Linux   (from setup.md)
    first-notebook.md            open, pick kernel, run, read a check, ask the tutor
    how-lessons-work.md          lesson → practice → exercise → project            (from setup.md)
    troubleshooting.md                                                             (from setup.md)
  paths/                         beginner.md, experienced.md, challenges.md, builder.md
  guides/
    learning-with-ai.md          (was docs/learning-with-ai.md) THE learner AI page: rule, study loop, prompts, red flags
    ai-setup.md                  (was docs/ai.md, minus the Author section) per-tool setup for Learn and Build modes only
    ai-prompts/                  (was docs/ai/) tutor-prompt.md, claude-project-instructions.md
    challenge-practice.md        (was docs/guides/challenge-practice.md) the method; the schedule lives in paths/challenges.md
    timed-session.md            (was docs/guides/timed-session.md)
  reference/
    course-map.md                (was docs/language.md)
    glossary.md                  new
  teaching/
    facilitator.md               (was docs/facilitator.md; paths/instructor.md merges into it)
  maintainers/
    README.md                    how the repo is built and tested, plus the Author mode from docs/ai.md
    concepts.md, upgrade-status.md, challenge-upgrade-status.md
    review/                      (moved from repo root in the last step, D18)
course/README.md, internals/README.md, patterns/README.md,
challenges/README.md, use-cases/README.md, solutions/README.md
.devcontainer/devcontainer.json  for Codespaces
```

Removed after their content moves: `docs/setup.md` (into get-started/), `docs/start-here.md` (into the README, `course/README.md` and the paths), `docs/ai.md` (into guides/ai-setup.md and maintainers/README.md).

`AGENTS.md` and `CLAUDE.md` stay at the root, because the tools look for them there. Update every path they mention.

**One page per job, and other pages link to it rather than repeat it:**
- How to learn with AI: `guides/learning-with-ai.md` only.
- How to set up each AI tool: `guides/ai-setup.md` only.
- The order of units: `course/README.md` only.

## Writing rules for every Markdown file

1. **The first lines say what the page is for and who it's for**, in at most two sentences.
2. **Breadcrumb at the top, next step at the bottom.** For example, `[Home](../../README.md) › [Get started](README.md) › Install` at the top and `**Next:** [Open your first notebook](first-notebook.md)` at the bottom. Remove the old `·`-separated nav bars. `learning-with-ai.md` already follows this format; keep it.
3. **One vocabulary**, defined once in the glossary:
   - *section*: one of the five top-level areas (Course, How Python works, Patterns, Challenges, Projects)
   - *path*: your route through the sections
   - *unit*: a numbered folder
   - *lesson*, *practice*, *exercise*, *project*, *explore page*, *problem*, *pattern*
   - *Part 1* (notebooks) and *Part 2* (programs), defined in `course/README.md`
   - *the tutor*: an AI tool set up with the repo's tutor prompt

   Don't use "track", "pass", "field" or "use case" in learner text. Keep "use-cases" as the folder name.
4. **Every command is in a code block, says where to type it** ("in a terminal, inside the `learn-python` folder"), and shows Mac/Linux and Windows versions where they differ.
5. **Define jargon the first time it appears and link it to the glossary:** terminal, repository, clone, virtual environment, uv, kernel, notebook, cell, package, pytest, PATH, Codespaces.
6. **Keep it short.** At most 600 words per page, except `reference/`, `teaching/` and `guides/learning-with-ai.md` (at most 1,000 words, kept whole). Split longer pages. Write headings as tasks or questions ("Install on Windows", "What if a check fails?").
7. **American spelling throughout.** Short sentences. Tables only when comparing things.
8. **No stale instructions.** Every instruction must match the repo as it is. Run a command before you document it.

## README content (at most 450 words)

1. `# Learn Python: understand how it works, then build with it`, a one-sentence description, the CI badge, and an **Open in GitHub Codespaces** badge linking `https://codespaces.new/RickZee/learn-python`.
2. **What you'll learn:** 5 bullets covering the language, how Python works, patterns and challenge problems, real projects, and learning with an AI tutor.
3. **Is this for you?** A 4-row table: never coded / know another language / preparing for timed challenges / want to build something → each links to its path.
4. **Start in 3 steps:** install (or open in Codespaces) → open your first notebook → do your first practice. Each step links to `docs/get-started/`.
5. **What's inside:** a table of the five sections plus `docs/`, with one line each. Then: "You can ignore `src/`, `tests/` and `tools/`. `solutions/` holds the answers; open one only after you've tried."
6. **Learning with AI:** two lines ("Use Cursor, Claude or any AI tool as a tutor: it explains, you write the code.") and a link to `docs/guides/learning-with-ai.md`.
7. License, how to report a problem (GitHub issue), and "Contributing" linking `docs/maintainers/README.md`.
