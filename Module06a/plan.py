"""Print DuckDB's measured physical plan for the dashboard."""
from pathlib import Path
import duckdb

parquet = Path(__file__).with_name("report_history.parquet")
con = duckdb.connect()
plan = con.execute(f"""EXPLAIN ANALYZE
SELECT machine_id, site, technician, SUM(part_price) AS cost
FROM read_parquet('{parquet}')
GROUP BY machine_id, site, technician""").fetchone()[1]
print(plan)
