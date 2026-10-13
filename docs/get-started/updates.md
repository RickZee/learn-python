[Home](../../README.md) › [Docs](../README.md) › Updates

# Keep your fork up to date

This course changes over time. If you cloned the main repo only, you can re-clone when you want a fresh copy. If you want to keep your practice work and still pull new lessons, use a *fork*.

A **fork** is your own copy of the repo on GitHub. A **branch** is a named line of commits inside that copy. **Upstream** is the original `RickZee/learn-python` remote you pull updates from.

## One-time setup

1. Fork [RickZee/learn-python](https://github.com/RickZee/learn-python) on GitHub.
2. Clone *your* fork (not the upstream URL):

   ```bash
   git clone https://github.com/<you>/learn-python.git
   cd learn-python
   ```

3. Add upstream so you can fetch course updates:

   ```bash
   git remote add upstream https://github.com/RickZee/learn-python.git
   ```

4. Work on a branch and commit after each session:

   ```bash
   git checkout -b my-work
   git add -A && git commit -m "session notes"
   ```

## Pull new lessons

```bash
git fetch upstream
git merge upstream/main
```

If Git reports a conflict in a notebook you edited, keep your version, then open the new upstream file beside it:

```bash
git checkout --ours path/to/notebook.ipynb
git show upstream/main:path/to/notebook.ipynb > new.ipynb
```

`new.ipynb` is only for reading. Copy anything useful into your notebook by hand, then delete `new.ipynb` and commit.

**Next:** [Open your first notebook](first-notebook.md)
