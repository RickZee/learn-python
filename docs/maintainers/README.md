[Home](../../README.md) › Maintainers

# Maintainers

This page is for people changing the course: adding lessons, fixing checks, or running the suite.

## How the repo is built and tested

From the repo root, in a terminal:

```bash
uv sync
uv run pytest -n auto
uv run ruff check .
```

Part 2 exercises and projects against reference solutions:

```bash
PYLEARN_SOLUTIONS=1 uv run pytest course use-cases
```

Refresh notebook outputs after you edit a lesson:

```bash
uv run python tools/refresh_outputs.py path/to/notebook.ipynb
```

Authoring rules live in [authoring.md](authoring.md). `AGENTS.md` at the repo root is the tutor/authoring router. Concept order is in [concepts.md](concepts.md). Pending guard paths: [status.md](status.md).

## Author mode (AI tools)

When you are changing the course, use the default mode: plain `claude`, or Cursor without the tutor rule. Leave the tutor off. If it is on, it will refuse to edit practice files.

Authoring plans and runbooks: [review/](review/).

**Next:** [Concept ledger](concepts.md)
