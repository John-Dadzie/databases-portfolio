# Module 6a — DuckDB analytical engine

Author: John Dadzie

## Evidence map

| Requirement | Evidence |
|---|---|
| Reproducible two-million-row history | [prepare.py](prepare.py) |
| SQLite-to-Parquet conversion and checksum | [to_parquet.py](to_parquet.py) |
| Interleaved median race | [race.py](race.py), results below |
| Measured DuckDB plan | [plan.py](plan.py) |
| OLTP boundary | [boundary.py](boundary.py) |
| Decision memo and freshness plan | [memo.md](memo.md) |
| Refresh verification | [refresh.py](refresh.py) |

## Results

`prepare.py` produced exactly **2,000,000 rows**. `to_parquet.py` produced the same row count and matching `SUM(part_price) = 49,000,000.00`, proving that the conversion did not change the dataset. The generated database was 112,660,480 bytes; the zstd Parquet file was 973,230 bytes. The generated database, CSV, and Parquet files are local build artefacts and are ignored by Git.

The interleaved five-run race produced:

```text
dashboard: sqlite=4709.8 ms [4509.3-5935.3] duckdb=32.2 ms [30.0-33.6] ratio=146.3x
monthly:   sqlite=2839.7 ms [2722.5-2932.2] duckdb=100.5 ms [80.7-121.0] ratio=28.3x
```

The important result is the measured ratio, not a universal millisecond claim: DuckDB wins the full-table aggregate because Parquet is columnar and the query reads only the needed columns. The monthly query has a smaller ratio because `strftime` runs for every row.

`EXPLAIN ANALYZE` showed a Parquet table scan reading the four projected columns across 2,000,000 rows, followed by projection and hash grouping; 17/17 row groups were scanned and the total reported time was 0.0722 s. SQLite's corresponding plan is `SCAN report_history` plus `USE TEMP B-TREE FOR GROUP BY`.

The boundary test showed SQLite is the correct engine for repeated single-row inserts and point lookups: SQLite measured 3.1 ms for inserts and 3.7 ms for lookups, while DuckDB measured 2,254.6 ms and 1,272.7 ms. DuckDB's per-statement overhead makes it slower there; batching helps but does not change the workload boundary.

`refresh.py --check` was run twice. Both runs reported `2,000,000` rows and `49,000,000.0`, so the refresh is reproducible and checked.

## Verification questions

- `range()` generates the ten history copies; shifting by 91 days preserves the intended quarter spacing.
- Row count plus a sum is stronger than file size alone: two files can have equal size while containing different values.
- A stale Parquet copy can produce an incorrect report, so refresh must be scheduled and checked with row count and sum.
- DuckDB is not a replacement for the operational SQLite database; it is the analytical copy.
