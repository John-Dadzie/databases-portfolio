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

`prepare.py` produced exactly **2,000,000 rows**. `to_parquet.py` produced the same row count and matching `SUM(part_price) = 21,000,000.00`, proving that the conversion did not change the dataset. The generated database was 112,660,480 bytes; the snappy Parquet file was 1,872,221 bytes and the zstd Parquet file was 970,527 bytes. The generated database, CSV, and Parquet files are local build artefacts and are ignored by Git.

The interleaved five-run race produced:

```text
dashboard: sqlite=4522.9 ms [3431.8-5246.9] duckdb=39.1 ms [38.7-39.6] ratio=115.6x
monthly:   sqlite=3105.8 ms [2699.2-5751.6] duckdb=97.1 ms [81.5-123.8] ratio=32.0x
```

The important result is the measured ratio, not a universal millisecond claim: DuckDB wins the full-table aggregate because Parquet is columnar and the query reads only the needed columns. The monthly query has a smaller ratio because `strftime` runs for every row.

`EXPLAIN ANALYZE` showed a Parquet table scan reading the four projected columns across 2,000,000 rows, followed by projection and hash grouping; 17/17 row groups were scanned and the total reported time was 0.0400 s. SQLite's corresponding plan is `SCAN report_history` plus `USE TEMP B-TREE FOR GROUP BY`.

The boundary test showed SQLite is the correct engine for repeated single-row inserts and point lookups: SQLite measured 2.3 ms for inserts and 2.8 ms for lookups, while DuckDB measured 1,325.4 ms and 872.3 ms. DuckDB's per-statement overhead makes it slower there. `executemany` reduced DuckDB's insert time to 731.6 ms, but batching still did not close the gap.

`refresh.py --check` was run twice:

```text
rows=2000000 checksum=21000000.0 parquet_bytes=970527 elapsed_ms=10251.6
rows=2000000 checksum=21000000.0 parquet_bytes=970527 elapsed_ms=10237.8
```

The script compares SQLite and Parquet row counts and checksums, returns status 1 on a mismatch, and removes its temporary CSV. The two successful runs show that the refresh is idempotent for the measured values; the elapsed time varies with the machine.

## Verification questions

- `range()` generates the ten history copies; shifting by 91 days preserves the intended quarter spacing.
- Row count plus a sum is stronger than file size alone: two files can have equal size while containing different values.
- A stale Parquet copy can produce an incorrect report, so refresh must be scheduled and checked with row count and sum.
- DuckDB is not a replacement for the operational SQLite database; it is the analytical copy.
