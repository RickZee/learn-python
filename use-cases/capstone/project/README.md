[Home](../../../README.md) › [Projects](../../README.md) › reading-list

# reading-list (capstone)

A reading list with one SQLite store, a CLI, a small HTTP API, CSV import, and a background job that fills missing titles from a mocked HTTP lookup. Keep Decide answers in [DECISIONS.md](DECISIONS.md) in this folder.
```bash
uv run pytest use-cases/capstone/project -k m1
uv run pytest use-cases/capstone/project -k m2
# …through m6
```

## M1 store

**What's new.** A SQLite-backed store: add a book by ISBN (title optional), list books, get by id.

**Uses:** [01 Paths](../../../course/14-files/01-paths-lesson.ipynb), [02 JSON](../../../course/14-files/02-json-lesson.ipynb) (shape of a row), [01 Classes](../../../course/11-classes/01-classes-lesson.ipynb).

**Behavior.** Duplicate ISBN raises a clear error. Empty list returns `[]`. Run `-k m1`.

**Decide:** Store ISBN as text or integer?

## M2 CLI

**What's new.** `readinglist add ISBN [--title TEXT]` and `readinglist list` over the same store.

**Uses:** [02 Main](../../../course/13-modules/02-main-lesson.ipynb), [02 Command line](../../02-command-line/README.md).

**Behavior.** Add prints the new id. List prints one book per line as `id isbn title`. Missing title shows `-`. Run `-k m2`.

**Decide:** Exit code 2 on duplicate ISBN, or 1?

## M3 CSV import

**What's new.** `import_csv(path)` reads `isbn,title` rows (title may be blank) into the store. Skip duplicate ISBNs with a warning count.

**Uses:** [03 CSV](../../../course/14-files/03-csv-lesson.ipynb), [01 Try except](../../../course/06-errors/01-try-except-lesson.ipynb).

**Behavior.** Returns `(added, skipped)`. A missing file raises a clear error. Run `-k m3`.

**Decide:** Fail the whole import on a ragged row, or skip that row?

## M4 HTTP API

**What's new.** FastAPI app: `POST /books`, `GET /books`, `GET /books/{id}` over the same store.

**Uses:** [04 Services](../../04-services/README.md), [notes-api](../../04-services/project/README.md).

**Behavior.** Unknown id → 404. Create returns 201. Run `-k m4`.

**Decide:** Accept title on create, or ISBN-only until enrichment?

## M5 enrich

**What's new.** A background-style job `enrich_missing(store, client)` fills blank titles via an HTTP lookup keyed by ISBN. Tests use `httpx.MockTransport`.

**Uses:** [05 Taskgroup](../../../course/17-concurrency/05-taskgroup-timeouts-lesson.ipynb) (shape of concurrent work), [price-watch fetch](../../12-scraping/project/README.md).

**Behavior.** Books that already have a title are left alone. A 404 from the lookup leaves the title blank. Run `-k m5`.

**Decide:** One request at a time, or a small pool?

## M6 status

**What's new.** Mark a book read/unread (`status`) from the CLI and API; list can filter by status.

**Uses:** [03 Dicts](../../../course/04-collections/03-dicts-lesson.ipynb), [01 Enums](../../../course/11-classes/05-enums-lesson.ipynb) (optional).

**Behavior.** Default status is `unread`. Invalid status → clear error / 422. Run `-k m6`.

**Decide:** Allow only `read`/`unread`, or also `reading`?

**Next:** [Projects](../../README.md)
