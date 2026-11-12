"""Compare 1,000 point writes/lookups in SQLite and DuckDB."""
import sqlite3
import time
import duckdb

N = 1000
rows = [(i, f"k{i}", i * 1.5) for i in range(N)]


def run_sqlite():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE s(id INTEGER PRIMARY KEY, k TEXT, v REAL)")
    start = time.perf_counter()
    for row in rows:
        con.execute("INSERT INTO s VALUES (?, ?, ?)", row)
    con.commit()
    insert = (time.perf_counter() - start) * 1000
    start = time.perf_counter()
    for i in range(N):
        con.execute("SELECT v FROM s WHERE id=?", (i,)).fetchone()
    return insert, (time.perf_counter() - start) * 1000


def run_duckdb():
    con = duckdb.connect()
    con.execute("CREATE TABLE s(id INTEGER PRIMARY KEY, k TEXT, v DOUBLE)")
    start = time.perf_counter()
    for row in rows:
        con.execute("INSERT INTO s VALUES (?, ?, ?)", row)
    insert = (time.perf_counter() - start) * 1000
    start = time.perf_counter()
    for i in range(N):
        con.execute("SELECT v FROM s WHERE id=?", (i,)).fetchone()
    return insert, (time.perf_counter() - start) * 1000


si, sl = run_sqlite()
di, dl = run_duckdb()
print(f"inserts sqlite {si:.1f} ms | duckdb {di:.1f} ms")
print(f"lookups sqlite {sl:.1f} ms | duckdb {dl:.1f} ms")
