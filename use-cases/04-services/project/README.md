[Home](../../../README.md) › [Projects](../../README.md) › notes-api

# notes-api

Store notes over HTTP. Keep Decide answers in `DECISIONS.md`.

```bash
uv run pytest use-cases/04-services/project -k m1
```

## M1 create list read

**What's new.** Create, list, and read notes (404 when missing).

**Uses:** [04 Services field](../README.md).

**Decide:** Auto-increment ids or UUIDs?

## M2 update delete

**What's new.** Update and delete; missing notes return 404.

**Decide:** PUT or PATCH for update?

## M3 validation

**What's new.** Title length 1–100 → HTTP 422.

**Decide:** Trim whitespace before checking length?

## M4 search page

**What's new.** `?q=` search plus `limit`/`offset` paging.

**Decide:** Search title only, or title and body?

## M5 tags

**What's new.** Tags on notes, filter by tag; store behind a `Protocol` with an in-memory fake in tests.

**Decide:** Tags as a list column or a join table?

**Next:** [Field](../README.md)
