# Module 1 notes

## Local-first decision

In my own words, when is SQLite a reasonable choice? When would a client/server database be justified?

My answer: SQLite is a good choice for a local app or tool that stores its data on one machine. A client/server database makes sense when many users or apps need to write to shared data over a network.

## Telemetry results

Total rows: 172,800
Rows per machine: cnc-01: 57,600; cnc-02: 57,600; cnc-03: 57,600
Peak vibration by machine: cnc-01: 2.398; cnc-02: 3.168; cnc-03: 2.55
Number of readings above 2.0: 11,714
Approximate database file size: about 10.5 MB (10,526,720 bytes)

## Bound parameters

What value did the example pass separately from the SQL text? Why is that useful?

My answer: The example passed the machine name cnc-02 separately from the SQL text. This keeps the value separate from the command, which is safer than building SQL by joining text together.

## AI-generated query check

Here is my SQLite table: readings(ts TEXT, machine TEXT, temp_c REAL, vib_rms REAL, spindle_load REAL). Write a query that returns, for each machine, the average spindle load for readings taken overnight (after 18:00), ordered by average load descending.

Did it run? What result did I inspect? Yes. The averages were cnc-03: 60.43, cnc-01: 60.37, and cnc-02: 60.36.

What did EXPLAIN QUERY PLAN report? SCAN readings; USE TEMP B-TREE FOR GROUP BY; USE TEMP B-TREE FOR ORDER BY.

One possible edge case: The query uses > '18:00:00', so it excludes readings taken at exactly 18:00. If those should count, use >= instead.

The AI got the table, average calculation, grouping, and descending sort right. I ran the query and checked all three results. EXPLAIN showed a full table scan and temporary structures for grouping and sorting. The boundary check reminded me that > excludes readings at exactly 18:00.

SELECT machine, AVG(spindle_load) AS avg_spindle_load
FROM readings
WHERE time(ts) > '18:00:00'
GROUP BY machine
ORDER BY avg_spindle_load DESC;