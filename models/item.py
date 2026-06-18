from models.base_model import BaseModel

class Item(BaseModel):
    table_name = "items"

    def get_all_with_location(self, include_deleted=False):
        query = """
            SELECT items.*, locations.name as location_name
            FROM items
            LEFT JOIN locations ON items.location_id = locations.id
        """
        if not include_deleted:
            query += " WHERE items.is_deleted = 0"
        return self.db.execute_query(query)

    def search(self, term):
        query = """
            SELECT items.*, locations.name as location_name
            FROM items
            LEFT JOIN locations ON items.location_id = locations.id
            WHERE items.is_deleted = 0 AND (
                items.name LIKE ? OR
                items.code LIKE ? OR
                items.category LIKE ?
            )
        """
        pattern = f"%{term}%"
        return self.db.execute_query(query, (pattern, pattern, pattern))

    def get_low_stock(self):
        query = """
            SELECT items.*, locations.name as location_name
            FROM items
            LEFT JOIN locations ON items.location_id = locations.id
            WHERE items.is_deleted = 0 AND items.current_stock <= items.min_stock
        """
        return self.db.execute_query(query)

    def update_stock(self, item_id, quantity_change):
        query = "UPDATE items SET current_stock = current_stock + ? WHERE id = ?"
        self.db.execute_query(query, (quantity_change, item_id), commit=True)

    def get_by_id(self, record_id):
        query = """
            SELECT items.*, locations.name as location_name
            FROM items
            LEFT JOIN locations ON items.location_id = locations.id
            WHERE items.id = ?
        """
        results = self.db.execute_query(query, (record_id,))
        return results[0] if results else None
