"""Replay-safe CSV ingestion using SQLite UPSERT."""
from __future__ import annotations

import csv
import sqlite3
import sys
from pathlib import Path

UPSERT = """
INSERT INTO reading(sensor_id, ts, value, interval_s)
VALUES (:sensor_id, :ts, :value, :interval_s)
ON CONFLICT(sensor_id, ts) DO UPDATE SET
    value = excluded.value,
    interval_s = excluded.interval_s
"""


def ingest(database: Path, source: Path) -> int:
    with source.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    values = [
        {
            "sensor_id": int(row["sensor_id"]),
            "ts": row["ts"],
            "value": float(row["value"]),
            "interval_s": int(row["interval_s"]),
        }
        for row in rows
    ]
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executemany(UPSERT, values)
    return len(values)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python Module04/ingest.py DB CSV")
    print(f"processed_rows: {ingest(Path(sys.argv[1]), Path(sys.argv[2]))}")
