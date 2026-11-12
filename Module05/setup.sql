-- Module 5, Round 3: reproducible ~200k-row denormalized source table
-- Run with: sqlite3 Module05/normalize.db ".read Module05/setup.sql"
-- Re-running this script replaces flat_jobpart and its machine index.

DROP TABLE IF EXISTS flat_jobpart;

CREATE TABLE flat_jobpart (
    job_id      INTEGER,
    machine_id  TEXT,
    site        TEXT,           -- machine_id -> site
    technician  TEXT,
    part_no     TEXT,
    part_price  TEXT,           -- intentionally TEXT for the normalization exercise
    done_on     TEXT
);

-- 20,000 jobs x exactly 10 parts = 200,000 job-part rows.
WITH RECURSIVE
    j(n) AS (
        SELECT 1
        UNION ALL
        SELECT n + 1 FROM j WHERE n < 20000
    ),
    p(k) AS (
        SELECT 1
        UNION ALL
        SELECT k + 1 FROM p WHERE k < 10
    )
INSERT INTO flat_jobpart (
    job_id, machine_id, site, technician, part_no, part_price, done_on
)
SELECT n,
       'cnc-' || printf('%02d', (n % 50) + 1),
       CASE (n % 50) WHEN 0 THEN 'Bielefeld' ELSE 'Gütersloh' END,
       'tech-' || (n % 7),
       'P-' || printf('%04d', (k % 40) + 1),
       printf('%.2f', 5 + (k % 40)),
       date('2026-01-01', '+' || (n % 90) || ' days')
FROM j CROSS JOIN p;

CREATE INDEX ix_flat_machine ON flat_jobpart(machine_id);

-- Validation: expected flat_rows = 200000.
SELECT COUNT(*) AS flat_rows FROM flat_jobpart;

-- Helpful profile for the next decomposition round:
-- expected jobs = 20000, machines = 50, distinct parts = 10.
SELECT COUNT(DISTINCT job_id) AS jobs,
       COUNT(DISTINCT machine_id) AS machines,
       COUNT(DISTINCT part_no) AS distinct_parts
FROM flat_jobpart;
