from models.item import Item
from models.audit_log import AuditLog
from utils.auth import AuthManager
from utils.barcode_gen import BarcodeGenerator

class ItemController:
    def __init__(self):
        self.item_model = Item()
        self.audit_log = AuditLog()

    def get_all_items(self):
        return self.item_model.get_all_with_location()

    def add_item(self, data):
        item_id = self.item_model.create(data)
        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Add Item", "items", item_id, f"Added item {data.get('name')}")

        # Auto-generate barcode if code is provided
        if data.get('code'):
            BarcodeGenerator.generate(data['code'], f"images/barcodes/{data['code']}")

        return item_id

    def update_item(self, item_id, data):
        self.item_model.update(item_id, data)
        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Update Item", "items", item_id)

    def delete_item(self, item_id):
        self.item_model.soft_delete(item_id)
        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Delete Item", "items", item_id)

    def search_items(self, term):
        return self.item_model.search(term)

    def get_low_stock(self):
        return self.item_model.get_low_stock()
