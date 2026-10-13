[Home](../../../README.md) › [Projects](../../README.md) › expenses

# expenses

Summarize a bank CSV with categories and budgets. Keep Decide answers in `DECISIONS.md`.

```bash
uv run pytest use-cases/08-data-analysis/project -k m1
```

## M1 rows

**What's new.** Parse each CSV row into a dataclass with a `Decimal` amount.

**Uses:** [02 Dataclasses](../../../course/11-classes/02-dataclasses-lesson.ipynb), [05 Floats](../../../course/10-pitfalls/05-floats-lesson.ipynb).

**Decide:** Store the date as a string or a `date`?

## M2 categories

**What's new.** Load category rules from a JSON file. Unmatched memos become `other`.

**Uses:** [02 JSON](../../../course/14-files/02-json-lesson.ipynb).

**Decide:** Match memo with `==` or `in`?

## M3 monthly

**What's new.** `monthly_totals(rows)` groups by `YYYY-MM` and category.

**Uses:** [03 Dicts](../../../course/04-collections/03-dicts-lesson.ipynb).

**Decide:** Include months with no spend?

## M4 bad rows

**What's new.** Bad rows report their line number and are not fatal for the rest.

**Uses:** [01 Try except](../../../course/06-errors/01-try-except-lesson.ipynb).

**Decide:** Skip bad rows, or fail the whole file after reporting?

## M5 budget

**What's new.** Compare monthly category totals to a budget file; list over-budget categories. Keep the chart helper.

**Uses:** [02 JSON](../../../course/14-files/02-json-lesson.ipynb).

**Decide:** Over budget on `>` or `>=`?

**Next:** [Field](../README.md)
