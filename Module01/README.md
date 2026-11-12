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

**Evidence:** [Module reflection](../Reflections/ref01.md).
An explanation of the course and assessment model still needs adding.

### LG2 — Portfolio

Set up a personal GitHub portfolio from the course template, with a
clean first commit and a .gitignore that keeps databases and secrets
out of Git.

**Evidence:** [GitHub portfolio](https://github.com/John-Dadzie/databases-portfolio),
[commit history](https://github.com/John-Dadzie/databases-portfolio/commits/main/),
and [.gitignore](../.gitignore).

### LG3 — Toolchain

Set up the entire toolchain reproducibly with uv: one fixed Python
plus SQLite, DuckDB, Datasette, and more, and verify it.

**Evidence:**
- [Python version setting](../.python-version)
- [Project configuration](../pyproject.toml)
- [Dependency lockfile](../uv.lock)
- [Verification script](../uv-check.py)
- [Verification output](uv-check-output.txt)
- [SQLite shell session](shell-tour.txt)

Python 3.14.9 and all five required project packages were detected.
The standalone SQLite shell also ran successfully.

### LG4 — Architecture

Explain, with a measurement, the difference between an embedded
database and a client/server database, and why most local apps
should not run a server.

**Evidence:** [Telemetry measurements and local-first notes](notes_template.md).

The recorded database contains 172,800 rows and occupies
10,526,720 bytes. Python accesses the SQLite file directly,
without a separate database server.

The architecture explanation and remaining task evidence still
need a final review.

### LG5 — Python

Load real rows into SQLite and query them from Python using
bound parameters.

**Evidence:**
- [Telemetry generator](generate_telemetry.py)
- [CSV-to-SQLite loader](load_telemetry.py)
- [Query checks](check_telemetry.py)
- [Results and bound-parameter explanation](notes_template.md)

### LG6 — Verification

Take a first LLM-generated query, run it, and begin the habit:
verify before you trust.

**Evidence:** [AI-query script](profile_ai_query.py) and
[verification notes](notes_template.md).

The saved notes include the prompt, SQL, results, query plan,
and a discussion of the 18:00 boundary.

## Task checklist

- [x] Create the GitHub portfolio repository.
- [x] Clone the repository locally.
- [ ] Finish personalizing the portfolio.
- [ ] Add pod members and links to their portfolios.
- [ ] Add the instructor as a collaborator.
- [x] Add and verify .gitignore.
- [x] Commit and push the initial portfolio changes.
- [x] Set up and verify the uv project environment.
- [x] Complete the SQLite shell tour and save its output.
- [x] Complete SQL Island and save a completion screenshot.
- [x] Write sql-island.md based on the game experience.
- [x] Run the local telemetry practice exercises.
- [x] Run and inspect an AI-generated SQL query.
- [x] Transfer scripts and notes into this portfolio.
- [ ] Check query timings and remaining telemetry evidence.
- [x] Write the Module 1 reflection.
- [ ] Commit and push the latest reflection and README updates.

## Personal profile

Still to write in my own words:
- Previous programming and SQL experience.
- Previous database, Python, terminal, and Git experience.
- What I hope to learn from this course.

## SQL Island

I completed SQL Island with step-by-step AI guidance.

- [Learning reflection and completion screenshot](sql-island.md)

## SQLite shell tour

Proves: LG3 — Toolchain

- [Captured shell session](shell-tour.txt)
- [SQL dump to rebuild the practice database](tour.sql)

Most useful dot-command: `.schema`.

I still need to explain in my own words why I found it useful.

## Collaboration and AI use

Tunay helped me set up VS Code.

ChatGPT assisted with setup, practice materials, SQL explanations,
and documentation drafts. I ran the suggested queries and checked
their results and feedback. This was guided practice.

Pod membership and portfolio links still need to be recorded.

## Reflection

[Read my Module 1 reflection](../Reflections/ref01.md)