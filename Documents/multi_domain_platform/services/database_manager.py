import sqlite3
from typing import Any

class DatabaseManager:
    """handling SQLite database connections and queries."""

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._connection = None

    def connect(self):
        """connecting to the database."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def close(self):
        """Closing the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, sql: str, params: Any = ()):
        """executing a write query (INSERT, UPDATE, DELETE)."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor

    def retrieve_one(self, sql: str, params: Any = ()):
        """retrieving a single row from the database."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def retrieve_all(self, sql: str, params: Any = ()):
        """retrieving all rows from the database."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]