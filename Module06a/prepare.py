"""Build a reproducible two-million-row history database and CSV."""
from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "history.db"
CSV = HERE / "report_history.csv"
BASE = HERE.parent / "Module05" / "normalize.db"

needs_bootstrap = not BASE.exists()
if BASE.exists():
    check = sqlite3.connect(BASE)
    needs_bootstrap = check.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='report_jobpart'"
    ).fetchone()[0] == 0 or check.execute(
        "SELECT COUNT(*) FROM report_jobpart"
    ).fetchone()[0] != 200_000
    check.close()
if needs_bootstrap:
    base = sqlite3.connect(BASE)
    base.execute("DROP TABLE IF EXISTS report_jobpart")
    base.executescript("""
    CREATE TABLE IF NOT EXISTS report_jobpart(
        job_id INTEGER, machine_id TEXT, site TEXT, technician TEXT,
        part_no TEXT, part_price REAL, done_on TEXT
    );
    WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n WHERE x<20000)
    INSERT INTO report_jobpart
    SELECT n.x, 'cnc-' || printf('%02d', (n.x%50)+1),
           CASE n.x%50 WHEN 0 THEN 'Bielefeld' ELSE 'Gütersloh' END,
           'tech-' || (n.x%7), 'P-' || printf('%04d', (n.x%10)+1),
           5.0 + (n.x%40), date('2026-01-01', '+' || (n.x%90) || ' days')
    FROM n CROSS JOIN (SELECT 1 AS p UNION ALL SELECT 2 UNION ALL SELECT 3
                       UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6
                       UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
                       UNION ALL SELECT 10);
    """)
    base.commit()
    base.close()

source = sqlite3.connect(BASE)
source.row_factory = sqlite3.Row
rows = source.execute("SELECT * FROM report_jobpart").fetchall()
if len(rows) != 200_000:
    raise SystemExit(f"expected 200000 source rows, found {len(rows)}")

DB.unlink(missing_ok=True)
connection = sqlite3.connect(DB)
connection.execute("""CREATE TABLE report_history(
    job_id INTEGER, machine_id TEXT, site TEXT, technician TEXT,
    part_no TEXT, part_price REAL, done_on TEXT)""")
for quarter in range(10):
    connection.executemany(
        "INSERT INTO report_history VALUES (?, ?, ?, ?, ?, ?, date(?, ?))",
        [
            (r["job_id"] + quarter * 1_000_000, r["machine_id"], r["site"],
             r["technician"], r["part_no"], r["part_price"], r["done_on"],
             f"+{quarter * 91} days")
            for r in rows
        ],
    )
connection.commit()
with CSV.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["job_id", "machine_id", "site", "technician",
                     "part_no", "part_price", "done_on"])
    writer.writerows(connection.execute("SELECT * FROM report_history"))
print("history rows:", connection.execute("SELECT COUNT(*) FROM report_history").fetchone()[0])
print("csv bytes:", CSV.stat().st_size)
connection.close()
source.close()
