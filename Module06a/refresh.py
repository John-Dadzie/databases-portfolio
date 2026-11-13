"""Rebuild Parquet from history.db and optionally verify row count and sum."""
from __future__ import annotations
import argparse
import csv
import sqlite3
import sys
import time
from pathlib import Path
import duckdb

HERE = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
start = time.perf_counter()
db = sqlite3.connect(HERE / "history.db")
parquet = HERE / "report_history.parquet"
csv_path = HERE / "_refresh.csv"
try:
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["job_id", "machine_id", "site", "technician", "part_no", "part_price", "done_on"])
        writer.writerows(db.execute("SELECT * FROM report_history"))
    sqlite_count, sqlite_total = db.execute(
        "SELECT COUNT(*), ROUND(SUM(part_price), 2) FROM report_history"
    ).fetchone()
finally:
    db.close()

con = duckdb.connect()
try:
    con.execute(
        f"COPY (SELECT * FROM read_csv_auto('{csv_path}', header=true)) "
        f"TO '{parquet}' (FORMAT parquet, COMPRESSION zstd)"
    )
    parquet_count, parquet_total = con.execute(
        f"SELECT COUNT(*), ROUND(SUM(part_price), 2) "
        f"FROM read_parquet('{parquet}')"
    ).fetchone()
finally:
    con.close()
    csv_path.unlink(missing_ok=True)

size = parquet.stat().st_size
elapsed = (time.perf_counter() - start) * 1000
print(
    f"rows={parquet_count} checksum={parquet_total} "
    f"parquet_bytes={size} elapsed_ms={elapsed:.1f}"
)
if args.check and (sqlite_count != parquet_count or sqlite_total != parquet_total):
    print(
        f"refresh check failed: sqlite rows={sqlite_count} checksum={sqlite_total}; "
        f"parquet rows={parquet_count} checksum={parquet_total}",
        file=sys.stderr,
    )
    raise SystemExit(1)
