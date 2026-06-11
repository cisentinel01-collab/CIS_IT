from database.db_manager import DBManager

class BaseModel:
    table_name = ""

    def __init__(self):
        self.db = DBManager()

    def get_all(self, include_deleted=False):
        query = f"SELECT * FROM {self.table_name}"
        if not include_deleted:
            # Check if is_deleted column exists for this table in schema
            # For simplicity, we assume it exists if we are using it
            query += " WHERE is_deleted = 0"
        return self.db.execute_query(query)

    def get_by_id(self, record_id):
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        results = self.db.execute_query(query, (record_id,))
        return results[0] if results else None

    def create(self, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        return self.db.execute_query(query, tuple(data.values()), commit=True)

    def update(self, record_id, data):
        set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        params = tuple(data.values()) + (record_id,)
        self.db.execute_query(query, params, commit=True)

    def soft_delete(self, record_id):
        query = f"UPDATE {self.table_name} SET is_deleted = 1 WHERE id = ?"
        self.db.execute_query(query, (record_id,), commit=True)

    def delete(self, record_id):
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        self.db.execute_query(query, (record_id,), commit=True)
