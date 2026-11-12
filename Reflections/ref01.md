# Reflection 1 — Introduction & Local-First Foundations

## Take-away

SQL Island helped me understand how a database can support a game.
SQL can retrieve information and change data, such as a character's
name, gold, or owned items. SELECT is the command I remember most.

My advice is to run a query, check its result, and understand what
changed before moving on.

## What was good?

Seeing the SQL results affect the game made the commands easier
to understand. I completed SQL Island with guidance and saved
a screenshot of completion.

I also set up my GitHub portfolio and saved my scripts and notes.

## What was difficult?

Setting up the tools involved several steps. Git, uv, and the SQLite
shell were initially unavailable in the terminal, so we installed
them and checked that they worked.

The game displayed translated English labels while its database
used German names. This caused confusion when writing queries.
I still need practice writing SQL independently.

## Exploration and show stoppers

I practised filtering, sorting, joining tables, calculating totals
and averages, and updating data.

The setup errors were resolved. I want to practise joins and
grouping further so I can explain and write them with less help.

## Interaction with peers and instructors

Tunay helped me set up VS Code.

## How did you verify AI suggestions?

I used ChatGPT for setup instructions, SQL suggestions, and explanations.

I ran the suggested commands and checked their output. For the
telemetry query, I inspected the results and EXPLAIN QUERY PLAN.
The plan showed a table scan and temporary B-trees for grouping
and sorting.

In SQL Island, an AI suggestion used the table name inhabitants.
The game reported that the table did not exist. Using the actual
table name, bewohner, fixed the error. This showed me that an
AI-generated query must be checked against the real database.

## Help and extra work

Tunay helped with VS Code setup. ChatGPT provided step-by-step
guidance and helped draft the documentation.

I completed the exercises with assistance. My next goal is to
repeat some queries without copying a suggested answer.