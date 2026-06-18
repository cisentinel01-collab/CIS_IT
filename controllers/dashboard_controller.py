from models.item import Item
from models.supplier import Supplier
from models.audit_log import AuditLog

class DashboardController:
    def __init__(self):
        self.item_model = Item()
        self.supplier_model = Supplier()
        self.audit_model = AuditLog()

    def get_dashboard_stats(self):
        items = self.item_model.get_all()
        suppliers = self.supplier_model.get_all()

        # Financial Stats
        from database.db_manager import DBManager
        db = DBManager()

        # Total Stock Value (Estimated from last purchase prices or average)
        # We'll calculate based on the movement_items last price for simplicity
        total_value = db.execute_query("SELECT SUM(i.current_stock * COALESCE((SELECT mi.price FROM movement_items mi WHERE mi.item_id = i.id ORDER BY mi.id DESC LIMIT 1), 0)) as total FROM items i")[0]['total'] or 0

        # Total IN and OUT values
        total_in = db.execute_query("SELECT SUM(final_total) as total FROM movements WHERE type = 'IN'")[0]['total'] or 0
        total_out = db.execute_query("SELECT SUM(final_total) as total FROM movements WHERE type = 'OUT'")[0]['total'] or 0

        # Performance Stats
        top_item = db.execute_query("""
            SELECT i.name, SUM(mi.quantity) as qty
            FROM movement_items mi
            JOIN items i ON mi.item_id = i.id
            JOIN movements m ON mi.movement_id = m.id
            WHERE m.type = 'OUT'
            GROUP BY i.id ORDER BY qty DESC LIMIT 1
        """)
        top_item_name = top_item[0]['name'] if top_item else "N/A"

        top_supplier = db.execute_query("""
            SELECT s.name, COUNT(m.id) as count
            FROM movements m
            JOIN suppliers s ON m.supplier_id = s.id
            WHERE m.type = 'IN'
            GROUP BY s.id ORDER BY count DESC LIMIT 1
        """)
        top_supplier_name = top_supplier[0]['name'] if top_supplier else "N/A"

        # Category Distribution
        cats = {}
        for i in items:
            cat = i['category'] or "غير مصنف"
            cats[cat] = cats.get(cat, 0) + i['current_stock']

        return {
            "total_items": len(items),
            "total_qty": sum(i['current_stock'] for i in items),
            "low_stock": len(self.item_model.get_low_stock()),
            "suppliers_count": len(suppliers),
            "category_data": cats,
            "stock_status": self.item_model.get_low_stock(),
            "total_value": total_value,
            "total_in": total_in,
            "total_out": total_out,
            "top_item": top_item_name,
            "top_supplier": top_supplier_name
        }

    def get_recent_activities(self):
        return self.audit_model.get_logs(limit=8)
