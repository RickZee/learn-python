[Home](../../../README.md) › [Projects](../../README.md) › ticket-triage

# ticket-triage

Label support tickets with a client you can fake in tests. Keep Decide answers in `DECISIONS.md`.

```bash
uv run pytest use-cases/09-machine-learning/project -k m1
```

## M1 classify

**What's new.** `classify_all` + `accuracy` with a `FakeClient`.

**Decide:** Fail open to `"unknown"` or re-raise after retries?

## M2 metrics

**What's new.** Confusion matrix and per-label precision/recall.

**Decide:** Micro or macro average for the headline score?

## M3 retry

**What's new.** Retry with backoff on a client that fails N times; give up → `"unknown"`.

**Decide:** Linear or exponential backoff?

## M4 concurrent

**What's new.** Classify concurrently with a bound on in-flight calls.

**Decide:** Thread pool or asyncio?

## M5 cache

**What's new.** Cache labels on disk keyed by a text hash.

**Decide:** Cache forever, or expire?

**Next:** [Field](../README.md)
