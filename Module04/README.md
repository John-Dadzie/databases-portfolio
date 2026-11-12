# Module 4 — Data Integrity, Constraints and Edge Triggers

Author: John Dadzie

| Requirement | Evidence |
|---|---|
| Study and acceptance evidence | [integrity-notes.md](integrity-notes.md) |
| Constrained schema | [setup.sql](setup.sql) |
| UPSERT ingestion | [ingest.py](ingest.py), [readings.csv](readings.csv) |
| Trigger cost | [trigger_bench.py](trigger_bench.py) |
| Read-only access | [access_demo.py](access_demo.py) |
| Reflection | [ref04.md](../Reflections/ref04.md) |

## Reproduce from the repository root

```powershell
sqlite3 Module04\edge.db ".read Module04\setup.sql"
python Module04\ingest.py Module04\edge.db Module04\readings.csv
python Module04\ingest.py Module04\edge.db Module04\readings.csv
python Module04\access_demo.py
python Module04\trigger_bench.py
```

`edge.db` is generated locally and ignored by Git; the reproducible SQL and evidence are included above.
