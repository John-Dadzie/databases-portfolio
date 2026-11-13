-- Module 5, Round 3: reproducible ~200k-row denormalized source table
-- Run with: sqlite3 Module05/normalize.db ".read Module05/setup.sql"
-- Re-running this script replaces flat_jobpart and its machine index.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS report_jobpart;
DROP TABLE IF EXISTS job_part;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS machine;
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

CREATE TABLE machine(
    machine_id TEXT PRIMARY KEY,
    site TEXT NOT NULL
);

CREATE TABLE part(
    part_no TEXT PRIMARY KEY,
    part_price REAL NOT NULL
);

CREATE TABLE job(
    job_id INTEGER PRIMARY KEY,
    machine_id TEXT NOT NULL REFERENCES machine(machine_id),
    technician TEXT NOT NULL,
    done_on TEXT NOT NULL
);

CREATE TABLE job_part(
    job_id INTEGER NOT NULL REFERENCES job(job_id),
    part_no TEXT NOT NULL REFERENCES part(part_no),
    PRIMARY KEY (job_id, part_no)
);

INSERT INTO machine
SELECT DISTINCT machine_id, site FROM flat_jobpart;

INSERT INTO part
SELECT DISTINCT part_no, CAST(part_price AS REAL) FROM flat_jobpart;

INSERT INTO job
SELECT DISTINCT job_id, machine_id, technician, done_on FROM flat_jobpart;

INSERT INTO job_part
SELECT DISTINCT job_id, part_no FROM flat_jobpart;

DROP TABLE IF EXISTS report_jobpart;
CREATE TABLE report_jobpart AS
SELECT j.job_id, m.machine_id, m.site, j.technician, jp.part_no,
       p.part_price, j.done_on
FROM job AS j
JOIN machine AS m ON m.machine_id = j.machine_id
JOIN job_part AS jp ON jp.job_id = j.job_id
JOIN part AS p ON p.part_no = jp.part_no;

CREATE INDEX ix_report_machine ON report_jobpart(machine_id);
