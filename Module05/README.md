# Module 5 — Normalization vs. denormalization

Author: John Dadzie

## Evidence map

| Requirement | Evidence |
|---|---|
| 200,000-row source and 3NF decomposition | [setup.sql](setup.sql) |
| Functional dependencies, ER sketches, and anomalies | [normalization-notes.md](normalization-notes.md) |
| Denormalized report DDL | [report-ddl.sql](report-ddl.sql) |
| Benchmark, row counts, storage, and query plans | [benchmark.py](benchmark.py), [benchmark-output.txt](benchmark-output.txt) |
| Recommendation and freshness strategy | [memo.md](memo.md) |
| Harvest curiosities and sources | [harvest.md](harvest.md) |
| Reflection | [ref05.md](../Reflections/ref05.md) |

## Reproduce

Run from the repository root:

```powershell
uv run python Module05\benchmark.py
```

The generated `normalize.db` is ignored by Git. The SQL, Python, captured
results, and written interpretation are the submission evidence.
