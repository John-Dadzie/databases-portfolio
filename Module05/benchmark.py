"""Build Module 5 designs and capture reproducible benchmark evidence."""

from __future__ import annotations

import pathlib
import sqlite3
import statistics
import time


ROOT = pathlib.Path(__file__).resolve().parent
DB = ROOT / "normalize.db"
SETUP = ROOT / "setup.sql"
OUTPUT = ROOT / "benchmark-output.txt"

NORMALIZED = """
SELECT m.machine_id, m.site, j.technician, SUM(p.part_price) AS cost
FROM job AS j
JOIN machine AS m ON m.machine_id = j.machine_id
JOIN job_part AS jp ON jp.job_id = j.job_id
JOIN part AS p ON p.part_no = jp.part_no
WHERE j.done_on >= date('2026-03-01')
GROUP BY m.machine_id, j.technician
"""

DENORMALIZED = """
SELECT machine_id, site, technician, SUM(part_price) AS cost
FROM report_jobpart
WHERE done_on >= date('2026-03-01')
GROUP BY machine_id, technician
"""


def timed(connection: sqlite3.Connection, query: str) -> float:
    start = time.perf_counter()
    connection.execute(query).fetchall()
    return (time.perf_counter() - start) * 1000


def plan(connection: sqlite3.Connection, query: str) -> list[str]:
    return [" ".join(str(value) for value in row) for row in connection.execute(
        "EXPLAIN QUERY PLAN " + query
    )]


def main() -> None:
    if DB.exists():
        DB.unlink()
    connection = sqlite3.connect(DB)
    connection.executescript(SETUP.read_text(encoding="utf-8"))
    connection.execute("PRAGMA foreign_keys = ON")

    counts = connection.execute(
        """
        SELECT
          (SELECT COUNT(*) FROM flat_jobpart),
          (SELECT COUNT(*) FROM machine),
          (SELECT COUNT(*) FROM part),
          (SELECT COUNT(*) FROM job),
          (SELECT COUNT(*) FROM job_part),
          (SELECT COUNT(*) FROM report_jobpart)
        """
    ).fetchone()
    if counts != (200000, 50, 10, 20000, 200000, 200000):
        raise RuntimeError(f"unexpected row counts: {counts}")

    normalized_rows = connection.execute(NORMALIZED).fetchall()
    denormalized_rows = connection.execute(DENORMALIZED).fetchall()
    if normalized_rows != denormalized_rows:
        raise RuntimeError("normalized and denormalized results differ")

    timed(connection, NORMALIZED)
    timed(connection, DENORMALIZED)
    normalized_times = [timed(connection, NORMALIZED) for _ in range(3)]
    denormalized_times = [timed(connection, DENORMALIZED) for _ in range(3)]

    before_machine = connection.total_changes
    connection.execute(
        "UPDATE machine SET site = 'Bielefeld' WHERE machine_id = 'cnc-02'"
    )
    machine_rows = connection.total_changes - before_machine
    before_report = connection.total_changes
    connection.execute(
        "UPDATE report_jobpart SET site = 'Bielefeld' WHERE machine_id = 'cnc-02'"
    )
    report_rows = connection.total_changes - before_report

    connection.execute("DROP INDEX ix_report_machine")
    without_index_ms = timed(connection, DENORMALIZED)
    connection.execute("CREATE INDEX ix_report_machine ON report_jobpart(machine_id)")

    normalized_bytes = connection.execute(
        """
        SELECT COALESCE(SUM(pgsize), 0) FROM dbstat
        WHERE name IN ('job', 'job_part', 'part', 'machine')
        """
    ).fetchone()[0]
    report_bytes = connection.execute(
        "SELECT COALESCE(SUM(pgsize), 0) FROM dbstat WHERE name = 'report_jobpart'"
    ).fetchone()[0]

    output = [
        "Module 5 benchmark evidence",
        f"counts: flat={counts[0]} machine={counts[1]} part={counts[2]} "
        f"job={counts[3]} job_part={counts[4]} report={counts[5]}",
        f"result rows: normalized={len(normalized_rows)} "
        f"denormalized={len(denormalized_rows)} equal=True",
        f"normalized_ms: {[round(value, 3) for value in normalized_times]} "
        f"median={statistics.median(normalized_times):.3f}",
        f"denormalized_ms: {[round(value, 3) for value in denormalized_times]} "
        f"median={statistics.median(denormalized_times):.3f}",
        f"site update rows: normalized={machine_rows} denormalized={report_rows}",
        f"denormalized_without_index_ms={without_index_ms:.3f}",
        f"storage_bytes: normalized={normalized_bytes} report={report_bytes}",
        "",
        "EXPLAIN QUERY PLAN normalized:",
        *plan(connection, NORMALIZED),
        "",
        "EXPLAIN QUERY PLAN denormalized:",
        *plan(connection, DENORMALIZED),
    ]
    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")
    connection.commit()
    connection.close()
    print("\n".join(output))


if __name__ == "__main__":
    main()
