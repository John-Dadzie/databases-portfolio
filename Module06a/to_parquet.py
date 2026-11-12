"""Convert the history CSV to Parquet with DuckDB."""
from pathlib import Path
import duckdb

HERE = Path(__file__).parent
CSV = HERE / "report_history.csv"
PARQUET = HERE / "report_history.parquet"
con = duckdb.connect()
con.execute(f"""
COPY (SELECT * FROM read_csv_auto('{CSV}', header=true))
TO '{PARQUET}' (FORMAT parquet, COMPRESSION zstd)
""")
count, total = con.execute(
    f"SELECT COUNT(*), ROUND(SUM(part_price), 2) FROM read_parquet('{PARQUET}')"
).fetchone()
print(f"parquet rows: {count}")
print(f"parquet sum: {total}")
print(f"parquet bytes: {PARQUET.stat().st_size}")
