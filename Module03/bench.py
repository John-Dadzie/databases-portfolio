"""Repeatable median benchmark for the Module 3 dashboard query."""

from __future__ import annotations

import statistics
import sqlite3
import time
from pathlib import Path


DB = Path(__file__).with_name("warehouse.db")
DASHBOARD = """
SELECT c.city, COUNT(DISTINCT c.customer_id) AS customers,
       SUM(ol.qty * p.price) AS revenue
FROM customer AS c
JOIN orders AS o ON o.customer_id = c.customer_id
JOIN order_line AS ol ON ol.order_id = o.order_id
JOIN product AS p ON p.product_id = ol.product_id
WHERE o.ordered_on >= '2025-01-01' AND o.ordered_on < '2026-01-01'
GROUP BY c.city
ORDER BY revenue DESC
"""
SINGLE_DAY = """
SELECT o.order_id, o.ordered_on, c.name
FROM orders AS o
JOIN customer AS c ON c.customer_id = o.customer_id
WHERE o.ordered_on = '2026-02-14'
"""


def median_ms(connection: sqlite3.Connection, query: str, runs: int = 3) -> float:
    times = []
    for _ in range(runs):
        started = time.perf_counter()
        connection.execute(query).fetchall()
        times.append((time.perf_counter() - started) * 1000)
    return statistics.median(times)


def plan(connection: sqlite3.Connection, query: str) -> list[str]:
    return [row[3] for row in connection.execute("EXPLAIN QUERY PLAN " + query)]


def main() -> None:
    if not DB.exists():
        raise SystemExit(f"{DB} not found; run sqlite3 {DB} .read Module03/setup.sql")

    indexes = [
        ("baseline", None),
        ("ix_orders_ordered_on", "CREATE INDEX ix_orders_ordered_on ON orders(ordered_on)"),
        ("ix_orderline_order", "CREATE INDEX ix_orderline_order ON order_line(order_id)"),
        ("ix_orderline_product", "CREATE INDEX ix_orderline_product ON order_line(product_id)"),
    ]
    index_names = [name for name, _ in indexes if name != "baseline"]

    with sqlite3.connect(DB) as connection:
        for name, create_index in indexes:
            for index_name in index_names:
                connection.execute(f"DROP INDEX IF EXISTS {index_name}")
            if create_index:
                connection.execute(create_index)
            print(f"{name}: {median_ms(connection, DASHBOARD):.3f} ms")
            for detail in plan(connection, DASHBOARD):
                print(f"  {detail}")

        connection.execute("DROP INDEX IF EXISTS ix_orders_ordered_on")
        before = median_ms(connection, SINGLE_DAY)
        before_plan = plan(connection, SINGLE_DAY)
        connection.execute("CREATE INDEX ix_orders_ordered_on ON orders(ordered_on)")
        after = median_ms(connection, SINGLE_DAY)
        after_plan = plan(connection, SINGLE_DAY)
        print(f"single_day_before: {before:.3f} ms")
        print(f"single_day_after: {after:.3f} ms")
        print(f"single_day_before_plan: {before_plan}")
        print(f"single_day_after_plan: {after_plan}")


if __name__ == "__main__":
    main()
