# Docs report (runbook 3)

## What moved where

| From | To |
| --- | --- |
| `docs/ai.md` | `docs/guides/ai-setup.md` (+ Author → `docs/maintainers/README.md`) |
| `docs/learning-with-ai.md` | `docs/guides/learning-with-ai.md` |
| `docs/ai/` | `docs/guides/ai-prompts/` |
| `docs/guides/challenge-practice.md` | `docs/guides/challenge-practice.md` |
| `docs/guides/timed-session.md` | `docs/guides/timed-session.md` |
| `docs/language.md` | `docs/reference/course-map.md` |
| `docs/facilitator.md` | `docs/teaching/facilitator.md` |
| `docs/concepts.md` | `docs/maintainers/concepts.md` |
| `docs/*upgrade-status.md`, `flow-upgrade-status.md` | `docs/maintainers/` |
| `docs/setup.md` | split into `docs/get-started/*` (deleted) |
| `docs/start-here.md` | folded into README, `course/README.md`, paths (deleted) |
| `docs/paths/instructor.md` | merged into `docs/teaching/facilitator.md` (deleted) |
| `review/` | `docs/maintainers/review/` (+ stub `review/README.md`) |

## Cold-start log (D11 / D18)

1. `git clone` from the local repo into a temp directory
2. `uv sync` (uv already on PATH)
3. `uv run python -c "import pylearn; print('ok')"` → `ok`
4. Executed `course/00-start/01-first-program-lesson.ipynb` with nbclient → success

## Untested

- `.devcontainer/devcontainer.json` was not built locally (devcontainer CLI not installed).
- Windows install steps were written from the official uv docs, not run on a Windows machine.

## Hardest pages for a newcomer

1. `docs/guides/learning-with-ai.md` — long, and easy to skim past the one rule
2. `docs/reference/course-map.md` — dense tables
3. `challenges/python-questions.md` — large question bank
4. `docs/guides/challenge-practice.md` — method is short; schedule lives on the path page
5. `use-cases/*/README.md` — many fields; easy to open too many at once
