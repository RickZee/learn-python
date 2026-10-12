[Home](../../README.md) › [Projects](../README.md) › Background jobs

# Background jobs

Work that must not block a web request: sending mail, resizing an image, rebuilding a report.

## Tools

- A queue such as Redis, SQS, or RabbitMQ
- Celery, RQ, or Dramatiq as the worker
- A retry with a limit, and a record of jobs that still fail

## Do this first

1. Open [01-lesson.ipynb](01-lesson.ipynb) and run it.
2. Retry a failing task twice, then record the error text, not only the name.
3. Keep the change small enough to finish in one sitting.

## Where it sits

Workers wait on other systems. That is [concurrency](../../course/17-concurrency/01-threads-lesson.ipynb).

**Next:** [Projects](../README.md)
