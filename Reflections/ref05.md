# Reflection 5 — Normalization vs. denormalization

## Take-away

Normalization is the safer operational design because each fact is changed once.
Denormalization is a measured read-model decision, not a universal performance
rule.

## What was good?

The reproducible 200,000-row build made the trade-off concrete. Comparing equal
results, query plans, storage, and rows changed was clearer than relying on a
general claim that one table is faster.

## What was difficult?

The difficult part was keeping the comparison fair: both queries needed the
same filter, warm-up, repeated runs, and result validation. The update test
also made the maintenance cost visible.

## Exploration and show stoppers

The index plan was a useful negative result because an index can add work when
the query reads nearly the whole report table. That finding belongs in the
decision record rather than being hidden.

## Interaction with peers and instructors

I used the module gate questions to check the candidate key, the three anomaly
examples, and why the normalized and denormalized row counts must match.

## How did you verify AI suggestions?

I treated suggestions as hypotheses and verified them with SQLite execution:
the setup produced 200,000 rows, the decomposition reproduced the report
results, foreign keys were enabled, and `EXPLAIN QUERY PLAN` plus repeated
timings supplied the performance evidence.

## Help and extra work

I added a reproducible benchmark, captured plans and storage, and documented
the refresh strategy so the evidence can be rerun instead of relying on
hand-copied numbers.
