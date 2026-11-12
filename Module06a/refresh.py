"""Rebuild Parquet from history.db and optionally verify row count and sum."""
from __future__ import annotations
import argparse
import csv
import sqlite3
from pathlib import Path
import duckdb

HERE = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
db = sqlite3.connect(HERE / "history.db")
parquet = HERE / "report_history.parquet"
csv_path = HERE / "_refresh.csv"
with csv_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["job_id", "machine_id", "site", "technician", "part_no", "part_price", "done_on"])
    writer.writerows(db.execute("SELECT * FROM report_history"))
db.close()
con = duckdb.connect()
con.execute(f"COPY (SELECT * FROM read_csv_auto('{csv_path}', header=true)) TO '{parquet}' (FORMAT parquet, COMPRESSION zstd)")
csv_path.unlink()
if args.check:
    count, total = con.execute(f"SELECT COUNT(*), ROUND(SUM(part_price),2) FROM read_parquet('{parquet}')").fetchone()
    print(f"check rows: {count}")
    print(f"check sum: {total}")
else:
    print(f"refreshed: {parquet.name}")
