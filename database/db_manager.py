import sqlite3
import os

class DBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.db_path = "database/wms_v2.db"
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        with open("database/schema.sql", "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

    def execute_query(self, query, params=(), commit=False):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if commit:
                conn.commit()
                return cursor.lastrowid

            # Convert sqlite3.Row to dict to avoid PySide6 issues
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
