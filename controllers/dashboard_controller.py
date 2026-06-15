from models.item import Item
from models.supplier import Supplier
from models.movement import Movement
from database.db_manager import DBManager

class DashboardController:
    def __init__(self):
        self.item_model = Item()
        self.supplier_model = Supplier()
        self.movement_model = Movement()
        self.db = DBManager()

    def get_stats(self):
        total_items = len(self.item_model.get_all())

        # Sum quantities
        qty_query = "SELECT SUM(current_stock) as total FROM items WHERE is_deleted = 0"
        qty_res = self.db.execute_query(qty_query)
        total_qty = qty_res[0]['total'] if qty_res and qty_res[0]['total'] else 0

        low_stock_count = len(self.item_model.get_low_stock())
        total_suppliers = len(self.supplier_model.get_all())

        # Recent activities (last 10 movements)
        recent_movements = self.movement_model.get_history()[:10]

        # Daily operations count
        from datetime import date
        today = date.today().isoformat()
        daily_ops_query = "SELECT COUNT(*) as total FROM movements WHERE date LIKE ?"
        daily_res = self.db.execute_query(daily_ops_query, (f"{today}%",))
        daily_ops = daily_res[0]['total'] if daily_res else 0

        # Inventory Value
        val_query = """
            SELECT SUM(i.current_stock * COALESCE(
                (SELECT price FROM movement_items mi
                 JOIN movements m ON mi.movement_id = m.id
                 WHERE mi.item_id = i.id AND m.type = 'IN'
                 ORDER BY m.date DESC LIMIT 1), 0)) as total_val
            FROM items i WHERE i.is_deleted = 0
        """
        val_res = self.db.execute_query(val_query)
        inventory_value = val_res[0]['total_val'] if val_res and val_res[0]['total_val'] else 0

        # Users count
        user_res = self.db.execute_query("SELECT COUNT(*) as count FROM users WHERE status != 'deleted'")
        users_count = user_res[0]['count'] if user_res else 0

        # Top issued item
        top_item_query = """
            SELECT i.name, SUM(mi.quantity) as total_qty
            FROM movement_items mi
            JOIN movements m ON mi.movement_id = m.id
            JOIN items i ON mi.item_id = i.id
            WHERE m.type = 'OUT'
            GROUP BY mi.item_id
            ORDER BY total_qty DESC LIMIT 1
        """
        top_item_res = self.db.execute_query(top_item_query)
        top_item = top_item_res[0]['name'] if top_item_res else "N/A"

        # Top 5 Suppliers
        top_suppliers_query = """
            SELECT s.name, COUNT(m.id) as op_count
            FROM suppliers s
            JOIN movements m ON s.id = m.supplier_id
            WHERE m.type = 'IN' AND s.is_deleted = 0
            GROUP BY s.id
            ORDER BY op_count DESC LIMIT 5
        """
        top_suppliers = self.db.execute_query(top_suppliers_query)

        # Top 5 Low Stock Items
        low_stock_items = self.item_model.get_low_stock()[:5]

        return {
            "total_items": total_items,
            "total_qty": total_qty,
            "low_stock_count": low_stock_count,
            "total_suppliers": total_suppliers,
            "recent_movements": recent_movements,
            "daily_ops": daily_ops,
            "inventory_value": inventory_value,
            "users_count": users_count,
            "top_item": top_item,
            "top_suppliers": top_suppliers,
            "low_stock_items": low_stock_items
        }
