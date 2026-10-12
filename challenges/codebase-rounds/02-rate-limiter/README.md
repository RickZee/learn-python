[Home](../../../README.md) › [Challenges](../../README.md) › Rate limiter

# Rate limiter

A 60-minute codebase round. An AI assistant is allowed. Run the tests after every suggestion, and write one sentence per change saying why it is correct.

```bash
uv run pytest challenges/codebase-rounds/02-rate-limiter
```

## Phase A. A planted race

`Limiter.allow` increments a shared counter from many threads. Without a lock, some allows are lost and the test fails.

## Phase B. Per-key windows

Each client key has its own count. Two keys must not share a counter. Fix the shared default dict bug.

## Phase C. Scale

`Limiter.allow` is called one million times for many distinct keys. A linear scan of history is too slow. Keep an O(1) counter per key.

## Modules

- `limiter/models.py` — a request stamp
- `limiter/window.py` — the sliding count
- `limiter/limiter.py` — `allow` and `reset`
- `limiter/report.py` — a one-line summary

**Next:** [Challenges](../../README.md)
