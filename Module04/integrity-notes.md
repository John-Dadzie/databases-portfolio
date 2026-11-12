# Module 4 — Integrity and edge triggers

Author: John Dadzie

## References and verified concepts

- [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html): enforcement is per connection, so `PRAGMA foreign_keys = ON` is required.
- [STRICT tables](https://www.sqlite.org/stricttables.html): declared types reject incompatible values.
- [Generated columns](https://www.sqlite.org/gencol.html): `energy_j` is computed consistently by SQLite.
- [UPSERT](https://www.sqlite.org/lang_upsert.html) and [triggers](https://www.sqlite.org/lang_createtrigger.html): replay-safe writes and automatic side effects.

Entity integrity uses primary keys, `NOT NULL`, and `UNIQUE`; referential integrity uses foreign keys; domain integrity uses `CHECK`, generated columns, and triggers. A `CHECK` cannot prove that a referenced row exists, so it cannot replace a foreign key.

## Acceptance test and exact rejections

The unconstrained table accepted `(1,'temp_c',9000)`, `(1,'temp_c','hot')`, and `(2,'bogus',-500)`. The constrained schema in [setup.sql](setup.sql) rejected:

| Test | Result |
|---|---|
| `value = 9000` | `CHECK constraint failed: value >= -273.15 AND value <= 5000` |
| `value = 'hot'` | `cannot store TEXT value in REAL column reading.value` |
| `sensor_id = 99` | `FOREIGN KEY constraint failed` |
| duplicate `(machine_id, metric)` | `UNIQUE constraint failed: sensor.machine_id, sensor.metric` |
| missing value | `NOT NULL constraint failed: reading.value` |

`CHECK` alone can accept `NULL`, so `NOT NULL` is also required. A valid row `(41.5, 1)` produces `energy_j = 41.5`.

## UPSERT evidence

The unique key `(sensor_id, ts)` makes this write idempotent:

```sql
INSERT INTO reading(sensor_id, ts, value, interval_s)
VALUES (:sensor_id, :ts, :value, :interval_s)
ON CONFLICT(sensor_id, ts) DO UPDATE SET
    value = excluded.value,
    interval_s = excluded.interval_s;
```

Running [ingest.py](ingest.py) twice with [readings.csv](readings.csv) processes six input rows but leaves exactly three database rows.

## Trigger evidence

`trg_vib_alarm` records `sensor_id=2, value=2.7, reason='vibration over 2.0 mm/s'`. Updating that reading from `2.7` to `1.4` creates an audit row with the old and new values. On the local run, the [trigger benchmark](trigger_bench.py) measured 10,000 inserts at 18.007 ms without the alarm trigger and 27.100 ms with it. The trigger adds write cost because it inserts one alarm per qualifying reading.

`AFTER INSERT` is the right default here: the reading has passed all constraints before the related alarm is recorded. A `BEFORE` trigger is better for rejecting or transforming input, but SQLite does not provide direct assignment to `NEW`.

## Access control without a server

[access_demo.py](access_demo.py) creates the `machine_health` view and proves that `file:...mode=ro` allows reads but returns `attempt to write a readonly database` for deletion. On Unix, `chmod 444 Module04/edge.db` and `chmod 644 Module04/edge.db` demonstrate file permissions; on Windows, equivalent NTFS/write-attribute settings apply.

PostgreSQL provides users, roles, and `GRANT SELECT` on a view. SQLite has no roles, so file permissions, safe views, and read-only connections are suitable for one local gateway but not for a multi-tenant web application where processes must have separate privileges.

## Agreed learning

Database errors are successful integrity checks. `STRICT`, `CHECK`, foreign keys, `UNIQUE`, UPSERT, and triggers solve different problems; none is a substitute for the others. Trigger cost must be measured when the write path is hot.
