# Module 5 harvest

## Curiosities

- The `CROSS JOIN` of 20,000 jobs and 10 parts creates exactly 200,000
  job-part rows. This makes the benchmark large enough to expose row width and
  index effects.
- `part_price` begins as `TEXT` in the deliberately flat source. The 3NF
  `part` table stores it as `REAL`, so the type matches its arithmetic use.
- `SELECT DISTINCT` is not a proof of the business rule. It only works here
  because the model assumes one machine and technician per job.
- `EXPLAIN QUERY PLAN` is evidence about the chosen access path, not a timing.
  The benchmark therefore records both plans and repeated warm timings.
- The report table repeats site, technician, and price. That can simplify reads,
  but it creates a freshness obligation and a larger update footprint.

## Sources

- SQLite `EXPLAIN QUERY PLAN`: https://www.sqlite.org/eqp.html
- SQLite `dbstat` virtual table: https://www.sqlite.org/dbstat.html
- Module 5 instructions: `professor modules/modules/05-normalization-vs-denormalization.md`
