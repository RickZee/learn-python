# Contributing

## Learners

Found a wrong lesson, a confusing explanation, or a broken setup step? Open an issue with one of the templates under **New issue** — do not open a PR that rewrites course notebooks unless a maintainer asked you to.

Keep your own answers in a fork or a `my-work` branch. See [Updating your fork](docs/get-started/updates.md).

## Reporting a problem

1. Pick the matching issue form: **Lesson is wrong**, **Explanation unclear**, or **Setup broke**.
2. Name the file path (for example `course/03-control-flow/02-loops-lesson.ipynb`).
3. Paste what you expected and what you got (traceback, screenshot, or exact wording).

That is enough. You do not need a proposed fix.

## Authoring and maintainers

Course authoring rules live under [`docs/maintainers/`](docs/maintainers/README.md), starting at [`authoring.md`](docs/maintainers/authoring.md). Review runbooks and progress files are in [`docs/maintainers/review/`](docs/maintainers/review/).

Say "I am authoring the course" (or point at a RUNBOOK / PROGRESS file) when working with an AI agent so it switches out of tutor mode.

## Checks before a maintainer PR

```bash
uv sync
uv run pytest -n auto && uv run ruff check . && uv run ruff format --check .
```

Against reference solutions when you touched exercises or projects:

```bash
PYLEARN_SOLUTIONS=1 uv run pytest course use-cases
```
