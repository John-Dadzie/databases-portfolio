# Memo — analytical copy recommendation

**To:** Lea Winter and Yasmin Kaya  
**Subject:** Moving the historical report to DuckDB/Parquet

Move the two-million-row historical reporting table to the Parquet copy and query it with DuckDB. Keep SQLite as the operational store for current writes, point lookups, and transactional updates. The interleaved median benchmark in [duckdb-notes.md](duckdb-notes.md) is the evidence for the aggregate decision; the boundary benchmark shows why DuckDB should not receive one-row-at-a-time application traffic. The Parquet file is smaller than the row-oriented database because it compresses columns together and reads only projected columns. Refresh it nightly after the operational shift with [refresh.py](refresh.py), then verify the row count and price sum. If the refresh fails or the checks change, mark the report stale and alert the owner instead of silently publishing it. A one-day-old copy is acceptable for month-end analysis only if the report displays its refresh timestamp; it is not acceptable for live operational decisions.
