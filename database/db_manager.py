import psycopg2
from psycopg2.extras import RealDictCursor
import os

class DBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.config = {
                'dbname': 'wms_erp',
                'user': 'wms_user',
                'password': 'wms_pass',
                'host': 'localhost',
                'port': '5432'
            }
        return cls._instance

    def get_connection(self):
        return psycopg2.connect(**self.config)

    def execute_query(self, query, params=(), commit=False):
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                    # For PostgreSQL, we might need a returning clause or use cursor.fetchone() for last row id
                    if "INSERT" in query.upper() and "RETURNING" in query.upper():
                        res = cursor.fetchone()
                        return res['id'] if res else None
                    return None

                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            conn.close()

    def execute_insert(self, query, params=()):
        """Helper for inserts that return ID"""
        if "RETURNING id" not in query.upper():
            query += " RETURNING id"
        return self.execute_query(query, params, commit=True)
