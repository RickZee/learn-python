[Home](../../../README.md) › [Projects](../../README.md) › tidy

# tidy

Sort a folder of files into subfolders by suffix. Build it one milestone at a time. Keep answers in `DECISIONS.md`.

```bash
uv run pytest use-cases/01-automation/project -k m1
```

## M1 plan

**What's new.** `plan(folder)` returns `(filename, suffix)` pairs sorted by name. Skip `undo.json`.

**Uses:** [01 Paths](../../../course/14-files/01-paths-lesson.ipynb), [01 Lists](../../../course/04-collections/01-lists-lesson.ipynb).

**Behavior.** Run `-k m1`.

**Decide:** Do files without a suffix belong in a folder named `_none`?

## M2 dry-run

**What's new.** `apply(folder, dry_run=True)` returns the plan and moves nothing.

**Uses:** [01 Decisions](../../../course/03-control-flow/01-decisions-lesson.ipynb).

**Behavior.** No `undo.json` on dry-run. Run `-k m2`.

**Decide:** Should dry-run print to stdout, or only return the plan?

## M3 apply

**What's new.** Real moves into `<suffix>/`. A name collision becomes `name (1).ext`.

**Uses:** [01 Paths](../../../course/14-files/01-paths-lesson.ipynb).

**Behavior.** Write `undo.json` with the moves. Run `-k m3`.

**Decide:** Start collision numbering at `(1)` or `(2)`?

## M4 undo

**What's new.** `undo(folder)` reads `undo.json` and restores files to the folder root.

**Uses:** [02 JSON](../../../course/14-files/02-json-lesson.ipynb).

**Behavior.** After undo, the suffix folders may be empty. Run `-k m4`.

**Decide:** Delete empty destination folders after undo?

## M5 hidden and summary

**What's new.** Skip hidden files (name starts with `.`). `summary(folder)` returns a table of suffix → count for the current plan.

**Uses:** [03 Formatting](../../../course/02-strings/03-formatting-lesson.ipynb).

**Behavior.** Run `-k m5`.

**Decide:** Is `.gitignore` hidden enough to skip, or only dotfiles?

**Next:** [Field](../README.md)
