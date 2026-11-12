# Module 2 — Data Contracts and Legacy Schemas

Author: John Dadzie

[← Portfolio](../README.md) |
[Official Module 2](../professors%20modules/modules/02-data-contracts-and-legacy-schemas.md)

## What I learned

This module taught me how to understand a database that has no reliable
documentation:

1. Read the tables and infer the entities and relationships.
2. Use SQL queries to prove data problems instead of only describing them.
3. Turn the corrected design into an executable data contract.

The original database is intentionally flawed. I did **not** silently repair
it. I first recorded what it contains in [er-audit.md](er-audit.md), then
designed the safer version in [contract.py](contract.py).

## Learning goals and evidence

| Goal | Evidence |
|---|---|
| Record study, sources, sketches, and pod learning | [study-log.md](study-log.md) |
| Reconstruct an ER model | [er-audit.md](er-audit.md), section 1 |
| Find integrity defects with SQL | [er-audit.md](er-audit.md), section 2 |
| Explain keys, cardinality, and normalization | [er-audit.md](er-audit.md), sections 1 and 3 |
| Write an executable contract | [contract.py](contract.py), [contract-ddl.sql](contract-ddl.sql) |
| Complete the stretcher work | [mermaid-lab.md](mermaid-lab.md) |
| Reflect on the work and verification | [reflection](../Reflections/ref02.md) |

## 1. Reproduce the legacy database

The setup is deliberately simple and repeatable:

```powershell
sqlite3 Module02/legacy.db ".read Module02/legacy_schema.sql"
```

The script creates four machines, four part rows (including a duplicate),
and four maintenance jobs (including an orphan job). It can be run again
because it drops the old tables first.

## 2. Main result

The old schema hides a many-to-many relationship in the text value
`parts_used = 'P-1001,P-1002'`. The corrected design uses the junction table
`job_part`, so each job/part pair is stored as one row.

Other important corrections are:

- every table has a primary key;
- maintenance jobs reference `machine_id`, not a machine name;
- part numbers are unique;
- prices use `NUMERIC(9, 2)`;
- dates use a date type and are required;
- foreign keys prevent orphan rows.

## 3. Run the contract

The contract contains both application validation (Pydantic) and database
constraints (SQLAlchemy):

```powershell
uv run python Module02/contract.py
```

The command validates one correct object, rejects one invalid object, creates
the corrected SQLite schema, and prints its tables.

The emitted DDL is saved in [contract-ddl.sql](contract-ddl.sql).

## 4. Clear conclusion

The legacy database can store data, but it cannot reliably explain or protect
that data. The audit queries show the defects; the contract makes the
intended rules explicit and enforceable.

