[Home](../../../README.md) › [Projects](../../README.md) › csvtool

# csvtool

A small CLI for CSV files. Build it one milestone at a time. After each milestone, answer the **Decide** question in a `DECISIONS.md` you keep in this folder.

```bash
uv run pytest use-cases/02-command-line/project -k m1
uv run pytest use-cases/02-command-line/project -k m2
# …and so on
```

## M1 count

**What's new.** `csvtool count FILE` prints the number of data rows (not the header).

**Uses:** [03 CSV](../../../course/14-files/03-csv-lesson.ipynb), [02 Main](../../../course/13-modules/02-main-lesson.ipynb).

**Behavior.** A header-only file prints `0`. Run `uv run pytest use-cases/02-command-line/project -k m1`.

**Decide:** Is a blank trailing line a row?

## M2 columns

**What's new.** `csvtool columns FILE` prints the header names, one per line, numbered from 1.

**Uses:** [04 Collections](../../../course/04-collections/).

**Behavior.** Numbering is for humans. Run `-k m2`.

**Decide:** 0- or 1-based numbering for humans?

## M3 filter

**What's new.** `csvtool count FILE --where COL=VALUE` (repeatable). Every `--where` must match.

**Uses:** [06 Errors](../../../course/06-errors/), [05 Unpacking](../../../course/05-functions/05-unpacking-and-keyword-only-lesson.ipynb).

**Behavior.** An unknown column exits with code 2 and `error: no column 'x'` on stderr. Run `-k m3`.

**Decide:** Case-sensitive matching?

## M4 bad input

**What's new.** Clear failures for bad files — never a traceback.

**Uses:** [02 Raise](../../../course/06-errors/02-raise-lesson.ipynb), [06 Custom exceptions](../../../course/11-classes/06-custom-exceptions-lesson.ipynb).

**Behavior.** A missing file, an empty file, or a ragged row (fewer fields than the header) each gives a clear stderr message and exit code 2. Run `-k m4`.

**Decide:** Skip ragged rows with a warning, or fail?

## M5 summary

**What's new.** `csvtool summary FILE COL` prints count, min, max, and mean for a numeric column. `--json` prints the same as JSON.

**Uses:** [02 JSON](../../../course/14-files/02-json-lesson.ipynb), [05 Floats](../../../course/10-pitfalls/05-floats-lesson.ipynb).

**Behavior.** Blank cells are skipped and counted. A non-number exits 2 and names the row. Run `-k m5`.

**Decide:** `float` or `Decimal`?

**Next:** [Field](../README.md)
