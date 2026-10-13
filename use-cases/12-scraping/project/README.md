[Home](../../../README.md) › [Projects](../../README.md) › price-watch

# price-watch

Parse prices from saved HTML, store history, and alert on drops. Keep Decide answers in `DECISIONS.md`.

```bash
uv run pytest use-cases/12-scraping/project -k m1
```

## M1 parse

**What's new.** `parse_price(html)` reads the `.price` text from a fixture.

**Uses:** [04 Text and bytes](../../../course/14-files/04-text-and-bytes-lesson.ipynb).

**Decide:** Return a string or a `Decimal`?

## M2 formats

**What's new.** Parse `$1,299.00`, `1.299,00 €`, and missing price → `None`.

**Uses:** [05 Regex](../../../course/02-strings/05-regex-lesson.ipynb).

**Decide:** Strip currency symbols before or after comma/dot normalization?

## M3 history

**What's new.** A watchlist JSON plus SQLite history of seen prices.

**Uses:** [02 JSON](../../../course/14-files/02-json-lesson.ipynb).

**Decide:** One table per item, or one table with an item id column?

## M4 alert

**What's new.** Alert when the price drops by at least X% vs the last seen price.

**Uses:** [01 Decisions](../../../course/03-control-flow/01-decisions-lesson.ipynb).

**Decide:** Alert on drop percentage from last seen or from all-time high?

## M5 fetch

**What's new.** Fetch with `httpx` using `MockTransport` in tests; polite delay between requests.

**Uses:** [01 Tooling](../../../course/18-tooling/01-tooling-lesson.ipynb).

**Decide:** Sleep even when the transport is mocked?

**Next:** [Field](../README.md)
