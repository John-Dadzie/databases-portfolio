"""Demonstrate SQL injection and its one correct fix: bound parameters."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DB = Path(__file__).with_name("warehouse.db")
if not DB.exists():
    raise SystemExit(f"{DB} not found; run the Module 3 setup first")


def vulnerable(connection: sqlite3.Connection, name: str) -> list[tuple[int, str]]:
    sql = f"SELECT customer_id, name FROM customer WHERE name = '{name}'"
    return connection.execute(sql).fetchall()


def safe(connection: sqlite3.Connection, name: str) -> list[tuple[int, str]]:
    sql = "SELECT customer_id, name FROM customer WHERE name = ?"
    return connection.execute(sql, (name,)).fetchall()


if __name__ == "__main__":
    with sqlite3.connect(DB) as connection:
        payload = "' OR '1'='1"
        print("normal:", vulnerable(connection, "Customer 1"))
        print("injected_count:", len(vulnerable(connection, payload)))
        print("safe:", safe(connection, payload))
