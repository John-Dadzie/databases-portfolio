# Module 3 study and verification notes

Author: John Dadzie

## References

| Source | Concept used |
|---|---|
| [SQLite EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) | A plan is evidence of scans, searches, covering indexes, and temporary B-trees. |
| [SQLite query planner](https://www.sqlite.org/queryplanner.html) | An index narrows a lookup but is not automatically beneficial for an aggregate-heavy query. |
| [OWASP SQL injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | Bound parameters keep user input separate from SQL syntax. |
| [Relational algebra](https://en.wikipedia.org/wiki/Relational_algebra) | Selection, projection, joins, and grouping describe the meaning behind SQL syntax. |

## LLM prompt, generated SQL, and verification

**Prompt:** “SQLite schema: `customer(customer_id, name, city)`, `product(product_id, sku, price)`, `orders(order_id, customer_id, ordered_on, status)`, `order_line(order_id, product_id, qty)`. Write a query that returns, for each city, the number of distinct customers and the total revenue (`qty*price`) of orders placed in 2025, ordered by revenue descending.”

**SQL produced and accepted after checking:**

```sql
SELECT c.city, COUNT(DISTINCT c.customer_id) AS customers,
       SUM(ol.qty * p.price) AS revenue
FROM customer AS c
JOIN orders AS o ON o.customer_id = c.customer_id
JOIN order_line AS ol ON ol.order_id = o.order_id
JOIN product AS p ON p.product_id = ol.product_id
WHERE o.ordered_on >= '2025-01-01' AND o.ordered_on < '2026-01-01'
GROUP BY c.city
ORDER BY revenue DESC;
```

I verified the distinct count, half-open date range, revenue expression, joins, and four-city output by running it against [warehouse.db](warehouse.db). The predicted outer operation was a scan of `order_line`; the actual plan confirmed it.

## Task A — plan safari

| Query | Prediction | Result before index | Result after `ix_job_tech` |
|---|---|---|---|
| `technician = 'Beier'` | SCAN | `SCAN maint_job` | `SEARCH maint_job USING INDEX ix_job_tech (technician=?)` |
| `machine_name = 'cnc-02'` | SCAN | `SCAN machine` | `SCAN machine` |
| `technician LIKE '%ei%'` | SCAN | `SCAN maint_job` | `SCAN maint_job` |

The equality predicate on the indexed column changes to a search. The other table has no index, and a leading wildcard prevents a normal B-tree index from narrowing the search. A function-wrapped predicate such as `lower(technician) = 'beier'` also remains a scan without an expression index.

## Task 1 — actual dashboard plan

```text
SCAN ol
SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY
```

The plan reads all 240,000 order lines, then uses integer primary-key lookups for the related rows. Temporary B-trees implement grouping, distinct counting, and final ordering.

## Task 2 — benchmark results

The reproducible benchmark is [bench.py](bench.py). Each value is the median of three executions on the same local database and process.

| State | Median dashboard time (ms) | Plan observation |
|---|---:|---|
| No index | 158.117 | `SCAN ol`; primary-key lookups; three temporary B-trees |
| `ix_orders_ordered_on` only | 152.133 | No dashboard plan change; scan remains cheaper than starting from the date index |
| `ix_orderline_order` only | 156.737 | No dashboard plan change; the planner still starts with `SCAN ol` |
| `ix_orderline_product` only | 156.014 | No dashboard plan change; product is reached through its primary key |

The exact milliseconds are machine-dependent; the plan change is the stronger evidence. The single-day lookup measured 4.200 ms before the index and 0.269 ms after it. Its plan changed from `SCAN o` to `SEARCH o USING INDEX ix_orders_ordered_on (ordered_on=?)`, confirming when the date index is useful.

## Task 3 — injection drill

The payload was:

```text
' OR '1'='1
```

Evidence: [injection_demo.py](injection_demo.py).

Representative output:

```text
normal: [(1, 'Customer 1')]
injected_count: 2000
safe: []
```

The vulnerable query treats the payload as SQL syntax and returns every customer. The parameterized query treats it as one value and returns no match. Escaping quotes by hand is not a complete fix because SQL has different literal contexts, encodings, and identifier/numeric cases; bound parameters keep the value out of the parser.

## Task 4 — relational algebra check

For the dashboard query, use `σ` for the 2025 selection, `⋈` for joins, `γ` for grouping/aggregation, and `π` for the final projection:

```text
π city, COUNT(DISTINCT customer_id)→customers, SUM(qty×price)→revenue
  γ city
    σ 2025-01-01 ≤ ordered_on < 2026-01-01
      (customer ⋈ orders ⋈ order_line ⋈ product)
```

The SQL has the same meaning: `JOIN ... ON` supplies the joins, `WHERE` supplies `σ`, `GROUP BY city` supplies `γ`, and the `SELECT` list supplies `π`. The SQL is written in a different order because SQL has a declarative syntax.

## Task 5 — window-function stretcher

### Grouped baseline

```sql
SELECT c.customer_id, c.name, COUNT(*) AS late_orders
FROM orders AS o
JOIN customer AS c ON c.customer_id = o.customer_id
WHERE o.status = 'late'
GROUP BY c.customer_id, c.name
ORDER BY late_orders DESC;
```

### Correlated subquery

```sql
SELECT c.customer_id, c.name,
       (SELECT COUNT(*)
        FROM orders AS o
        WHERE o.customer_id = c.customer_id
          AND o.status = 'late') AS late_orders
FROM customer AS c
WHERE EXISTS (
    SELECT 1 FROM orders AS o
    WHERE o.customer_id = c.customer_id AND o.status = 'late'
)
ORDER BY late_orders DESC;
```

### Window function

```sql
SELECT customer_id, name, late_orders
FROM (
    SELECT c.customer_id, c.name,
           COUNT(*) OVER (PARTITION BY c.customer_id) AS late_orders
    FROM orders AS o
    JOIN customer AS c ON c.customer_id = o.customer_id
    WHERE o.status = 'late'
)
GROUP BY customer_id, name, late_orders
ORDER BY late_orders DESC;
```

The grouped query is clearest for one row per customer. The correlated form repeats a lookup conceptually and is easiest to understand as “count late rows for this customer.” The window form keeps row-level data while adding the partition count, but needs a final deduplication step here. The LLM defaulted to the grouped query, which is the best fit for this report.

The measured plan shapes were:

```text
grouped:
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR ORDER BY

correlated:
SCAN c
SEARCH o EXISTS USING AUTOMATIC PARTIAL COVERING INDEX (customer_id=? AND status=?)
CORRELATED SCALAR SUBQUERY
USE TEMP B-TREE FOR ORDER BY

window:
CO-ROUTINE (subquery-1)
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR ORDER BY
```

## Agreed learning and curiosities

- `SCAN` versus `SEARCH` describes the access path; timing alone cannot explain why.
- An index can change a plan and still make an aggregate query slower.
- `COUNT(DISTINCT ...)` must be checked explicitly; a plausible `COUNT(*)` is a correctness bug.
- A leading wildcard and a function around a column commonly defeat a simple index.
- The `%`-formatted SQL in [injection_demo.py](injection_demo.py) is the collected “looks harmless” curiosity; it is unsafe because input becomes SQL syntax.

