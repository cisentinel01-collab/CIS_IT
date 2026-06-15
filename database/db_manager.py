import sqlite3
import os

class DBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.db_path = "database/wms.db"
            cls._instance.init_db()
        return cls._instance

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        if not os.path.exists("database/schema.sql"):
            return

        with open("database/schema.sql", "r", encoding="utf-8") as f:
            schema_script = f.read()

        conn = self.get_connection()
        try:
            conn.executescript(schema_script)
            conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

    def execute_query(self, query, params=(), commit=False):
        conn = self.get_connection()
        cursor = conn.cursor()
        result = None
        try:
            cursor.execute(query, params)
            if commit:
                conn.commit()
                result = cursor.lastrowid
            else:
                rows = cursor.fetchall()
                # Convert sqlite3.Row to dict to avoid Shiboken conversion issues
                result = [dict(row) for row in rows]
        except Exception as e:
            print(f"Database error: {e}")
            if commit:
                conn.rollback()
        finally:
            conn.close()
        return result

    def execute_many(self, query, params_list, commit=True):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(query, params_list)
            if commit:
                conn.commit()
        except Exception as e:
            print(f"Database error: {e}")
            if commit:
                conn.rollback()
        finally:
            conn.close()
