from models.base_model import BaseModel

class Movement(BaseModel):
    table_name = "movements"

    def create_movement(self, movement_data, items_list):
        """
        movement_data: dict with movement headers
        items_list: list of dicts with {'item_id': id, 'quantity': q, 'price': p}
        """
        movement_id = self.create(movement_data)

        for item in items_list:
            item_query = "INSERT INTO movement_items (movement_id, item_id, quantity, price) VALUES (?, ?, ?, ?)"
            self.db.execute_query(item_query, (movement_id, item['item_id'], item['quantity'], item.get('price', 0)), commit=True)

            # Update item stock
            stock_change = item['quantity'] if movement_data['type'] == 'IN' else -item['quantity']
            update_stock_query = "UPDATE items SET current_stock = current_stock + ? WHERE id = ?"
            self.db.execute_query(update_stock_query, (stock_change, item['item_id']), commit=True)

        return movement_id

    def get_movement_details(self, movement_id):
        query = """
            SELECT mi.*, i.name as item_name, i.code as item_code, i.unit
            FROM movement_items mi
            JOIN items i ON mi.item_id = i.id
            WHERE mi.movement_id = ?
        """
        return self.db.execute_query(query, (movement_id,))

    def get_history(self, type=None, start_date=None, end_date=None):
        query = "SELECT m.*, s.name as supplier_name FROM movements m LEFT JOIN suppliers s ON m.supplier_id = s.id WHERE 1=1"
        params = []
        if type:
            query += " AND m.type = ?"
            params.append(type)
        if start_date:
            query += " AND m.date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND m.date <= ?"
            params.append(end_date)
        query += " ORDER BY m.date DESC"
        return self.db.execute_query(query, tuple(params))
