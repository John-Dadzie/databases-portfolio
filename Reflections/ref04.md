# Reflection 4 — Data Integrity, Constraints and Edge Triggers

## Take-away

The database should reject invalid edge data before it spreads. `STRICT`, `CHECK`, foreign keys, unique keys, generated columns, UPSERT, and triggers each protect a different part of the data contract.

## What was good?

Seeing the same invalid rows accepted by an unconstrained table and rejected by the constrained schema made the value of database-side rules clear. The UPSERT replay test also showed how a unique natural key turns unreliable delivery into safe ingestion.

## What was difficult?

The most difficult point was remembering that `PRAGMA foreign_keys` is per connection. The schema can contain a foreign key while a connection still accepts an orphan row if it does not enable enforcement.

## Exploration and show stoppers

The trigger experiment showed that integrity is not free: the alarm trigger adds work to every matching insert. That cost is acceptable when the alarm must exist immediately, but it should be measured on a hot ingest path.

## Interaction with peers and instructors

I organized the evidence around the module's four required demonstrations: rejected rows, replay-safe ingestion, alarm/audit triggers, and read-only access. The results are in [Module04/integrity-notes.md](../Module04/integrity-notes.md).

## How did you verify AI suggestions?

I checked each suggested rule by running a real insert and recording the exact SQLite result. I also ran the UPSERT twice, queried the generated `energy_j`, triggered an alarm, updated a reading for the audit row, and tested a read-only connection.

## Help and extra work

I completed the reproducible schema, ingestion script, trigger benchmark, access-control demonstration, and trigger-timing explanation as the portfolio evidence for this module.
