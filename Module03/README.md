# Module 3 — LLM-Assisted SQL and Query Profiling

Author: John Dadzie

[← Portfolio](../README.md) |
[Official Module 3](../professors%20modules/modules/03-llm-assisted-sql-and-query-profiling.md)

## Submission evidence

| Requirement | Evidence |
|---|---|
| Study log, references, LLM verification, and plan safari | [sql-notes.md](sql-notes.md) |
| Reproducible warehouse dataset | [setup.sql](setup.sql) |
| LLM query, predicted and actual plan | [sql-notes.md](sql-notes.md), Task 1 |
| Median index benchmark and negative result | [bench.py](bench.py), [sql-notes.md](sql-notes.md), Task 2 |
| SQL injection and parameterized fix | [injection_demo.py](injection_demo.py), [sql-notes.md](sql-notes.md), Task 3 |
| Relational algebra translation | [sql-notes.md](sql-notes.md), Task 4 |
| Window-function stretcher | [sql-notes.md](sql-notes.md), Task 5 |
| Reflection | [ref03.md](../Reflections/ref03.md) |

## Reproduce

From the repository root:

```powershell
sqlite3 Module03\warehouse.db ".read Module03\setup.sql"
python Module03\bench.py
python Module03\injection_demo.py
```

The setup creates 2,000 customers, 500 products, 60,000 orders, and 240,000 order lines. The generated database is intentionally ignored by Git; [setup.sql](setup.sql) is the reproducible evidence.
