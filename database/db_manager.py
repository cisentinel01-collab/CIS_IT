import psycopg2
from psycopg2.extras import RealDictCursor
import os

class DBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            # Load from environment variables for security
            cls._instance.config = {
                'dbname': os.getenv('DB_NAME', 'wms_erp'),
                'user': os.getenv('DB_USER', 'wms_user'),
                'password': os.getenv('DB_PASS', 'wms_pass'),
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': os.getenv('DB_PORT', '5432')
            }
        return cls._instance

    def get_connection(self):
        try:
            return psycopg2.connect(**self.config)
        except Exception as e:
            print(f"Database Connection Error: {e}")
            raise e

    def execute_query(self, query, params=(), commit=False):
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                    # If it's an INSERT with RETURNING, fetch the ID
                    if "RETURNING" in query.upper():
                        try:
                            res = cursor.fetchone()
                            return res['id'] if res and 'id' in res else None
                        except:
                            return None
                    return None

                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            conn.close()
