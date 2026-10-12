[Home](../../README.md) › [Projects](../README.md) › APIs and services

# APIs and services

Programs other programs call. A request comes in as data. A response goes out as data, usually JSON, with a status code.

## Tools

- FastAPI or Flask for HTTP
- pydantic for the shape of a request
- OpenAPI so clients can generate their own code
- gRPC when the callers are services and latency matters

## Do this first

1. Open [01-lesson.ipynb](01-lesson.ipynb) and run it.
2. Reject a body whose title is empty, and return a different status from a missing field.
3. Keep the change small enough to finish in one sitting.

## Where it sits

Put slow work in [background jobs](../05-background-jobs/README.md). Check behavior with [tests](../../course/15-testing/01-unittest-lesson.ipynb).

**Next:** [Projects](../README.md)
