[Home](../../README.md) › [Projects](../README.md) › Databases

# Databases

Data that outlives one run of the program, and that more than one request can read.

## Tools

- sqlite3, which ships with Python, for one file
- PostgreSQL through psycopg, often with SQLAlchemy
- Redis for a fast cache
- A migration so the table shape is versioned

## Do this first

1. Open [01-lesson.ipynb](01-lesson.ipynb) and run it.
2. Insert a third row, update one amount, and select only the updated row.
3. Keep the change small enough to finish in one sitting.

## Where it sits

The pipeline that fills the table is [data engineering](../07-data-engineering/README.md).

**Next:** [Projects](../README.md)
