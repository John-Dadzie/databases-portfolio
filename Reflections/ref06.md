# Reflection 6 — The Analytical Engine

## Take-away

DuckDB and Parquet are a strong analytical copy, not a replacement for the operational SQLite database. The correct choice depends on the workload.

## What was good?

The two-million-row comparison made the difference measurable: DuckDB was about 146 times faster for the dashboard aggregate on this run. The point-write test was equally useful because it showed the reversal instead of presenting DuckDB as universally better.

## What was difficult?

The hardest part was keeping the comparison honest: both engines needed the same row count, same sum, warmed runs, and interleaved timing. A single timing would have mixed cache effects with engine behavior.

## How did you verify AI suggestions?

I verified the generated history with a row count and price sum, checked the Parquet conversion, read DuckDB's `EXPLAIN ANALYZE`, compared SQLite's plan, and ran the refresh check twice. I kept the measured negative result for single-row inserts and lookups.

## Decision

The Parquet copy should be refreshed nightly and checked before reports are published. SQLite keeps current writes and point lookups; DuckDB handles large historical aggregates. The decision and staleness plan are recorded in [Module06a/memo.md](../Module06a/memo.md).
