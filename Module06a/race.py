"""Interleaved median comparison of SQLite and DuckDB on the same data."""
from __future__ import annotations
import sqlite3
import statistics
import time
from pathlib import Path
import duckdb

HERE = Path(__file__).parent
SQLITE = sqlite3.connect(HERE / "history.db")
DUCK = duckdb.connect()
PARQUET = HERE / "report_history.parquet"
QUERIES = {
    "dashboard": """SELECT machine_id, site, technician, SUM(part_price) AS cost
                    FROM {source} WHERE done_on >= '2026-01-01'
                    GROUP BY machine_id, site, technician""",
    "monthly": """SELECT strftime(done_on, '%Y-%m') AS month, machine_id,
                  COUNT(*) AS jobs, SUM(part_price) AS cost
                  FROM {source} GROUP BY month, machine_id"""
}


def timed(function) -> float:
    start = time.perf_counter()
    function()
    return (time.perf_counter() - start) * 1000


for name, query in QUERIES.items():
    sqlite_run = lambda: SQLITE.execute(query.format(source="report_history")).fetchall()
    duck_run = lambda: DUCK.execute(
        query.format(source=f"read_parquet('{PARQUET}')")).fetchall()
    sqlite_run()
    duck_run()
    sqlite_times = [timed(sqlite_run) for _ in range(5)]
    duck_times = [timed(duck_run) for _ in range(5)]
    print(f"{name}: sqlite={statistics.median(sqlite_times):.1f} ms "
          f"[{min(sqlite_times):.1f}-{max(sqlite_times):.1f}] "
          f"duckdb={statistics.median(duck_times):.1f} ms "
          f"[{min(duck_times):.1f}-{max(duck_times):.1f}] "
          f"ratio={statistics.median(sqlite_times)/statistics.median(duck_times):.1f}x")
