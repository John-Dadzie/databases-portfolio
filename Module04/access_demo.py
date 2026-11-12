"""Demonstrate a safe view and a read-only SQLite connection."""
from pathlib import Path
import sqlite3

database = Path(__file__).with_name("edge.db")
with sqlite3.connect(database) as connection:
    connection.execute("""
        CREATE VIEW IF NOT EXISTS machine_health AS
        SELECT s.machine_id, s.metric, MAX(r.value) AS peak, COUNT(*) AS n
        FROM sensor s JOIN reading r USING(sensor_id)
        GROUP BY s.machine_id, s.metric
    """)

with sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True) as connection:
    print("readonly_count:", connection.execute("SELECT COUNT(*) FROM reading").fetchone()[0])
    try:
        connection.execute("DELETE FROM reading")
    except sqlite3.OperationalError as error:
        print("readonly_delete:", error)
