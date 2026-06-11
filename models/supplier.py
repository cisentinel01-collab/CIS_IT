from models.base_model import BaseModel

class Supplier(BaseModel):
    table_name = "suppliers"

    def search(self, term):
        query = f"SELECT * FROM {self.table_name} WHERE is_deleted = 0 AND (name LIKE ? OR phone LIKE ? OR email LIKE ?)"
        pattern = f"%{term}%"
        return self.db.execute_query(query, (pattern, pattern, pattern))
