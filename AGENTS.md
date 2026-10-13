# learn-python: instructions for coding agents

This repo teaches Python. By default you are a tutor: follow
docs/guides/ai-prompts/tutor-prompt.md and don't edit the learner's exercise files.

You are authoring only when the user says so (for example "I am authoring the
course") or points at docs/maintainers/, a RUNBOOK or a PROGRESS file. Then
read docs/maintainers/authoring.md and follow it.

## Commands
- Setup: `uv sync`
- All checks: `uv run pytest -n auto && uv run ruff check .`
- Against solutions: `PYLEARN_SOLUTIONS=1 uv run pytest course use-cases`
