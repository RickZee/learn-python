[Home](../../../README.md) › [Challenges](../../README.md) › Library checkout

# Library checkout

A 60-minute codebase round. An AI assistant is allowed. Run the tests after every suggestion, and write one sentence per change saying why it is correct.

```bash
uv run pytest challenges/codebase-rounds/01-library-checkout
```

## Phase A. A shared list

Two patrons must not see each other's loans. One test fails because a default list is shared.

## Phase B. Holds

Add a holds queue. The first person to join is the first person served.

## Phase C. Scale

`Store.find` is called on a catalog of 100,000 books. A linear scan is too slow. Add an index.

## Modules

- `library/models.py` — a book
- `library/store.py` — the catalog
- `library/loans.py` — checkout
- `library/holds.py` — the queue
- `library/report.py` — a one-line summary

**Next:** [Challenges](../../README.md)
