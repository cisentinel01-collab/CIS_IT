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
        total_qty = qty_res[0]['total'] if qty_res[0]['total'] else 0

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

        return {
            "total_items": total_items,
            "total_qty": total_qty,
            "low_stock_count": low_stock_count,
            "total_suppliers": total_suppliers,
            "recent_movements": recent_movements,
            "daily_ops": daily_ops
        }
