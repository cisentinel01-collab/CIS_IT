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
        return {
            "total_items": len(items),
            "total_qty": sum(i['current_stock'] for i in items),
            "low_stock": len(self.item_model.get_low_stock()),
            "suppliers_count": len(self.supplier_model.get_all()),
        }

    def get_recent_activities(self):
        return self.audit_model.get_logs(limit=10)
