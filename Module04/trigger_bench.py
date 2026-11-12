"""Measure the write cost of the vibration alarm trigger."""
from __future__ import annotations

import statistics
import sqlite3
import time

SCHEMA = """
CREATE TABLE sensor(sensor_id INTEGER PRIMARY KEY, machine_id TEXT, metric TEXT, unit TEXT) STRICT;
CREATE TABLE reading(reading_id INTEGER PRIMARY KEY, sensor_id INTEGER, ts TEXT, value REAL, interval_s INTEGER,
                    energy_j REAL GENERATED ALWAYS AS (value * interval_s) VIRTUAL) STRICT;
CREATE TABLE alarm(alarm_id INTEGER PRIMARY KEY, sensor_id INTEGER, ts TEXT, value REAL, reason TEXT) STRICT;
INSERT INTO sensor VALUES (2, 'cnc-01', 'vib_rms', 'mm/s');
"""
TRIGGER = """
CREATE TRIGGER trg_vib_alarm AFTER INSERT ON reading FOR EACH ROW
WHEN NEW.value > 2.0
BEGIN
    INSERT INTO alarm(sensor_id, ts, value, reason)
    VALUES(NEW.sensor_id, NEW.ts, NEW.value, 'vibration over 2.0 mm/s');
END;
"""


def measure(connection: sqlite3.Connection, rows: list[tuple[int, str, float, int]]) -> float:
    connection.execute("DELETE FROM reading")
    connection.execute("DELETE FROM alarm")
    started = time.perf_counter()
    connection.executemany(
        "INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (?, ?, ?, ?)",
        rows,
    )
    connection.commit()
    return (time.perf_counter() - started) * 1000


with sqlite3.connect(":memory:") as connection:
    connection.executescript(SCHEMA)
    rows = [
        (2, f"2026-03-01 08:{n // 60:02d}:{n % 60:02d}", 2.7, 1)
        for n in range(10_000)
    ]
    without_trigger = statistics.median(measure(connection, rows) for _ in range(3))
    connection.executescript(TRIGGER)
    with_trigger = statistics.median(measure(connection, rows) for _ in range(3))
    print(f"without_trigger_ms: {without_trigger:.3f}")
    print(f"with_trigger_ms: {with_trigger:.3f}")
    print(f"alarm_rows: {connection.execute('SELECT COUNT(*) FROM alarm').fetchone()[0]}")
