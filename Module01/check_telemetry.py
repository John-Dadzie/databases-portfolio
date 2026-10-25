"""Run the Module 1 questions and a bound-parameter example on telemetry.db."""

import sqlite3
from pathlib import Path


def show_query(connection, title, sql, parameters=()):
    print("\n" + title)
    cursor = connection.execute(sql, parameters)
    if cursor.description:
        columns = [item[0] for item in cursor.description]
        print(" | ".join(columns))
        print("-" * 68)
        for row in cursor.fetchall():
            print(" | ".join(str(value) for value in row))


def main():
    database_path = Path(__file__).with_name("telemetry.db")
    if not database_path.exists():
        raise FileNotFoundError("Run generate_telemetry.py and load_telemetry.py first.")

    connection = sqlite3.connect(database_path)
    try:
        show_query(
            connection,
            "1) Reading count per machine",
            "SELECT machine, COUNT(*) AS n FROM readings GROUP BY machine ORDER BY machine",
        )
        show_query(
            connection,
            "2) Peak vibration per machine",
            "SELECT machine, MAX(vib_rms) AS peak_vib FROM readings GROUP BY machine ORDER BY machine",
        )
        show_query(
            connection,
            "3) Number of readings above 2.0 mm/s",
            "SELECT COUNT(*) AS alarm_readings FROM readings WHERE vib_rms > ?",
            (2.0,),
        )
        show_query(
            connection,
            "4) Bound parameter example: readings for one machine",
            "SELECT machine, COUNT(*) AS n FROM readings WHERE machine = ? GROUP BY machine",
            ("cnc-02",),
        )
        show_query(
            connection,
            "5) Query plan for the bound lookup",
            "EXPLAIN QUERY PLAN SELECT * FROM readings WHERE machine = ?",
            ("cnc-02",),
        )
    finally:
        connection.close()

    print("\nWrite down what each result means in notes_template.md.")


if __name__ == "__main__":
    main()
