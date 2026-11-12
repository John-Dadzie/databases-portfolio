# Reflection 2 — Data Contracts and Legacy Schemas

## What I learned

I learned that a database can contain useful rows and still have an unsafe
design. The maintenance jobs looked understandable, but the missing keys,
duplicate part number, invalid date, orphan job, and comma-separated parts
made the data unreliable.

## What was difficult

The hardest part was separating what the old schema **stores** from what the
designer probably **intended**. For example, `parts_used` looks like one
column, but it actually represents a many-to-many relationship.

## How I verified my work

I recreated the database from
[legacy_schema.sql](../Module02/legacy_schema.sql) and ran the five queries in
[er-audit.md](../Module02/er-audit.md). I checked that each query returned the
expected bad row. I also ran `uv run python Module02/contract.py` to verify
that the corrected contract validates data and creates the four tables.

## Main conclusion

The best audit result is not just a list of problems. It connects each
problem to a query and then to a constraint in the corrected design.
