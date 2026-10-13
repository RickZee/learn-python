[Home](../../README.md) › [Docs](../README.md) › Install

# Install

This page gets you a working copy of the repo. Pick **No install** if you want to start in the browser, or follow Mac, Windows, or Linux below.

## No install (Codespaces)

1. Open [github.com/codespaces/new/RickZee/learn-python](https://codespaces.new/RickZee/learn-python) while signed into GitHub.
2. Create the codespace. The first build often takes 5–10 minutes while it installs uv and runs `uv sync`.
3. When the editor opens, continue with [your first notebook](first-notebook.md).

GitHub gives a limited pool of free Codespaces hours each month. If the free hours run out, use a local install below.

## Mac or Linux

Type these in a [terminal](../reference/glossary.md), inside the folder where you keep projects.

**Get the code** (pick one):

```bash
git clone https://github.com/RickZee/learn-python.git
cd learn-python
```

Or download the ZIP from GitHub, unzip it, and `cd` into the `learn-python` folder.

**Install uv**, then sync:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart the terminal (or open a new tab) so `uv` is on your PATH, then:

```bash
uv sync
```

## Windows

Type these in **PowerShell**, inside the folder where you keep projects.

**Get the code** (pick one):

```powershell
git clone https://github.com/RickZee/learn-python.git
cd learn-python
```

Or download the ZIP from GitHub, unzip it, and `cd` into the `learn-python` folder.

**Install uv**, then sync:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close PowerShell and open it again so `uv` is on your PATH, then:

```powershell
uv sync
```

## Pick an editor

- **VS Code** or **Cursor**: open the `learn-python` folder.
- **JupyterLab** (optional), from the repo folder:

```bash
uv run --with jupyter jupyter lab
```

## Check it worked

In a terminal, inside the `learn-python` folder:

```bash
uv run python -c "import pylearn; print('ok')"
```

You should see `ok`.

**Next:** [Keep your fork up to date](updates.md) · [Open your first notebook](first-notebook.md)
