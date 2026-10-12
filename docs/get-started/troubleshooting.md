[Home](../../README.md) › [Docs](../README.md) › Troubleshooting

# Troubleshooting

Fixes for the problems people hit first.

## `uv` not found (Windows)

Close the terminal and open a new one after installing uv so PATH updates. In PowerShell, check with:

```powershell
uv --version
```

If it still fails, sign out of Windows and back in, then retry.

## `ModuleNotFoundError: No module named 'pylearn'`

The notebook is using the wrong [kernel](../reference/glossary.md). Choose **Python Environments → `.venv`** in this folder, then run the cell again. Prefer `uv run` for terminal commands so they use the same environment.

## The kernel isn't listed

From the repo folder, in a terminal:

```bash
uv sync
```

Then reload the window in VS Code or Cursor and open **Select Kernel** again.

## Codespaces is still building

The first create often takes 5–10 minutes. Wait for the terminal to finish `postCreateCommand`. If it failed, open the Codespaces log, then rebuild the container.

## conda or Homebrew Python is first on PATH

That does not change `.venv`. Use `uv run` for commands and the `.venv` kernel for notebooks.

## Notebook cells were run out of order

A later cell can fail because an earlier one never ran. Use **Restart Kernel**, then run from the top, or run All above.

## A check fails

Read the last line of the error first. Fix your function, run the cell again. Open hints in order only when stuck.

## The tutor wrote the answer anyway

Confirm the Learn-mode setup in [AI setup](../guides/ai-setup.md), and turn off autocomplete (Cursor Tab, Copilot) while you practice.

## Run the repo checks

From the repo root, in a terminal:

```bash
uv run pytest
```

**Next:** [How lessons work](how-lessons-work.md) if you have not read it yet, or [Learning with an AI tutor](../guides/learning-with-ai.md)
