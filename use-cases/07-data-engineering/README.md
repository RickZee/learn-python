[Home](../../README.md) › [Projects](../README.md) › Data engineering

# Data engineering

Pipelines that move data from a source, change its shape, and land it where analysts or services can read it.

## Tools

- pandas or polars for tables
- pyarrow and Parquet for columnar files
- SQLAlchemy or a warehouse driver for the database
- Airflow, Dagster, or Prefect to run the pipeline on a schedule

## Do this first

1. Open [01-lesson.ipynb](01-lesson.ipynb) and run it.
2. Drop two different kinds of bad row, and count how many you dropped.
3. Keep the change small enough to finish in one sitting.

## Where it sits

Clean rows land in a [database](../11-databases/README.md) or a table an [analyst](../08-data-analysis/README.md) reads.

**Next:** [Projects](../README.md)
