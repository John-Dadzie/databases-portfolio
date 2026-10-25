# Module 1 — Introduction & Local-First Foundations

Author: John Dadzie

[← Portfolio](../README.md) |
[Official Module 1](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/01-introduction-and-local-first.md)

## Exploration plan

Explore how SQLite stores machine telemetry locally, query it from
Python, and verify AI-generated SQL using results and query plans.

## Learning Goals

### LG1 — Course

Explain how this class works: the CBL/PBL philosophy, portfolio-based
project work assessment, and the “moving bar” of a first-time course.

**Evidence:** Course understanding and personal reflection still to add.

### LG2 — Portfolio

Set up a personal GitHub portfolio from the course template, with a
clean first commit and a .gitignore that keeps databases and secrets
out of Git.

**Evidence:** Repository created and cloned; customization in progress.
The .gitignore and first personal commit still need checking.

### LG3 — Toolchain

Set up the entire toolchain reproducibly with uv: one fixed Python
plus SQLite, DuckDB, Datasette, and more, and verify it.

**Evidence:** Pending. Running the practice scripts alone does not
verify the required uv environment.

### LG4 — Architecture

Explain, with a measurement, the difference between an embedded
database and a client/server database, and why most local apps
should not run a server.

**Evidence:** Local telemetry measurements are saved in the practice
folder and still need transferring and reviewing.

### LG5 — Python

Load real rows into SQLite and query them from Python using
bound parameters.

**Evidence:** Telemetry scripts and results are saved in the practice
folder and still need transferring into this portfolio.

### LG6 — Verification

Take a first LLM-generated query, run it, and begin the habit:
verify before you trust.

**Evidence:** SQL, query results, EXPLAIN QUERY PLAN output, and
verification notes are saved locally and still need transferring.

## Task checklist

- [x] Create the GitHub portfolio repository.
- [x] Clone the repository locally.
- [ ] Finish personalizing the portfolio.
- [ ] Add pod members and links to their portfolios.
- [ ] Add the instructor as a collaborator.
- [ ] Add and verify .gitignore.
- [ ] Commit and push the portfolio changes.
- [ ] Set up and verify the uv environment.
- [ ] Complete the SQLite shell tour and save its output.
- [ ] Play SQL Island and save a progress screenshot.
- [ ] Write sql-island.md based on the actual game experience.
- [x] Run the local telemetry practice exercises.
- [x] Run and inspect an AI-generated SQL query.
- [ ] Transfer scripts and notes into this portfolio.
- [ ] Check query timings and remaining telemetry evidence.
- [ ] Write the Module 1 reflection.

## Personal profile

Still to write in my own words:
- Previous programming and SQL experience.
- Previous database, Python, terminal, and Git experience.
- What I hope to learn from this course.

## Collaboration and AI use

AI assisted with setup, practice materials, and drafting documentation.
I will record collaborators and sources, review the drafts, and
explain how I checked the code and SQL results.

## Reflection

The Module 1 reflection still needs to be written.

## SQLite shell tour

Proves: LG3 — Toolchain

- [Captured shell session](shell-tour.txt)
- [SQL dump to rebuild the practice database](tour.sql)

Most useful dot-command: .schema