from pathlib import Path
import sqlite3

database = Path(__file__).with_name("telemetry.db")

query = """
SELECT machine, AVG(spindle_load) AS avg_spindle_load
FROM readings
WHERE time(ts) > '18:00:00'
GROUP BY machine
ORDER BY avg_spindle_load DESC
"""

with sqlite3.connect(database) as connection:
    print("Query results:")
    for machine, average in connection.execute(query):
        print(f"{machine}: {average:.2f}")

    print("\nQuery plan:")
    for row in connection.execute("EXPLAIN QUERY PLAN " + query):
        print(row[3])