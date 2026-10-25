import sys
import platform
import sqlite3
from importlib.metadata import version, PackageNotFoundError

print("uv-managed Python:", sys.executable)
print("Python:", platform.python_version())
print("SQLite:", sqlite3.sqlite_version)

for package in ("duckdb", "datasette", "sqlite-utils", "pydantic", "sqlalchemy"):
    try:
        print(f"{package}: {version(package)}")
    except PackageNotFoundError:
        print(f"{package}: NOT INSTALLED")