"""Load the generated CSV into a local SQLite database using Python's stdlib."""

import csv
import sqlite3
from pathlib import Path


def main():
    folder = Path(__file__).parent
    csv_path = folder / "telemetry.csv"
    database_path = folder / "telemetry.db"
    if not csv_path.exists():
        raise FileNotFoundError("Run generate_telemetry.py first to create {}".format(csv_path.name))

    with sqlite3.connect(database_path) as connection:
        connection.executescript(
            """
            DROP TABLE IF EXISTS readings;
            CREATE TABLE readings(
                ts TEXT NOT NULL,
                machine TEXT NOT NULL,
                temp_c REAL NOT NULL,
                vib_rms REAL NOT NULL,
                spindle_load REAL NOT NULL
            );
            """
        )
        with csv_path.open(newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            connection.executemany(
                "INSERT INTO readings VALUES (?, ?, ?, ?, ?)", reader
            )
        count = connection.execute("SELECT COUNT(*) FROM readings").fetchone()[0]

    print("Loaded {:,} rows into {}.".format(count, database_path))
    print("Expected count: 172,800 (57,600 readings for each of 3 machines).")


if __name__ == "__main__":
    main()
