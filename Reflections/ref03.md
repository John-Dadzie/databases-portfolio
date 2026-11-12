# Reflection 3 — LLM-Assisted SQL and Query Profiling

## Take-away

An LLM can produce SQL that runs while still being wrong or inefficient. I must check the result, the query plan, and the security boundary before trusting it.

## What was good?

The warehouse dataset made the difference between a full scan and an indexed lookup visible. The benchmark was also useful because it showed that an index can change a plan without making an aggregate query faster.

## What was difficult?

The difficult part was interpreting the plan as a loop nest rather than treating `SEARCH` as automatically good. The aggregate query reads many order lines, so an index can add lookup work instead of removing it.

## Exploration and show stoppers

The injection payload was a clear demonstration: string concatenation changed the meaning of the query, while the bound parameter returned no rows. The leading-wildcard and function-wrapped predicates were useful negative examples for indexing.

## Interaction with peers and instructors

I compared the predicted plan with the actual SQLite output and recorded the differences in [Module03/sql-notes.md](../Module03/sql-notes.md). The shared conclusion was that plans are stronger evidence than a single timing.

## How did you verify AI suggestions?

I asked an LLM to write the per-city 2025 revenue query and to suggest indexes. I checked the date range, distinct customer count, joins, result, and `EXPLAIN QUERY PLAN` output against the generated warehouse. I tested each suggested index separately and kept the negative result instead of changing the measurement.

## Help and extra work

I completed the reproducible setup, benchmark, injection demonstration, algebra translation, and window-function comparison as the portfolio evidence for this module.
