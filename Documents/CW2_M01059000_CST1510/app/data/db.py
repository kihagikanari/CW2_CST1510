from pathlib import Path
import sqlite3

DATA_DIR = Path("DATA")
DB_PATH = "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the database file if it doesn't exist.

    Args:
        db_path: Path to the database file

    Returns:
        sqlite3.Connection: Database connection object
    """
    return sqlite3.connect(str(db_path))

conn = connect_database()
print("connected successfully")
