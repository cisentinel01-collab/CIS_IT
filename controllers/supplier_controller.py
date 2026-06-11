from models.supplier import Supplier
from models.audit_log import AuditLog
from utils.auth import AuthManager

class SupplierController:
    def __init__(self):
        self.supplier_model = Supplier()
        self.audit_log = AuditLog()

    def get_all_suppliers(self):
        return self.supplier_model.get_all()

    def add_supplier(self, data):
        supplier_id = self.supplier_model.create(data)
        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Add Supplier", "suppliers", supplier_id)
        return supplier_id

    def update_supplier(self, supplier_id, data):
        self.supplier_model.update(supplier_id, data)
        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Update Supplier", "suppliers", supplier_id)

    def delete_supplier(self, supplier_id):
        self.supplier_model.soft_delete(supplier_id)
        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Delete Supplier", "suppliers", supplier_id)

    def search_suppliers(self, term):
        return self.supplier_model.search(term)
