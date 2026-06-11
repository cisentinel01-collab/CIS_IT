from models.movement import Movement
from models.audit_log import AuditLog
from models.settings import Settings
from utils.auth import AuthManager
from utils.pdf_gen import PDFGenerator
import datetime

class StockController:
    def __init__(self):
        self.movement_model = Movement()
        self.audit_log = AuditLog()
        self.settings_model = Settings()
        self.pdf_gen = PDFGenerator()

    def receive_stock(self, movement_data, items_list):
        # Add timestamp if not provided
        if 'date' not in movement_data:
            movement_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        movement_data['type'] = 'IN'

        movement_id = self.movement_model.create_movement(movement_data, items_list)

        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Stock In", "movements", movement_id)

        # Generate PDF Invoice
        self.generate_movement_pdf(movement_id)

        return movement_id

    def issue_stock(self, movement_data, items_list):
        if 'date' not in movement_data:
            movement_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        movement_data['type'] = 'OUT'

        movement_id = self.movement_model.create_movement(movement_data, items_list)

        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Stock Out", "movements", movement_id)

        # Generate PDF Voucher
        self.generate_movement_pdf(movement_id)

        return movement_id

    def generate_movement_pdf(self, movement_id):
        movement = self.movement_model.get_by_id(movement_id)
        # Fetch supplier name if it exists
        if movement['supplier_id']:
            from models.supplier import Supplier
            supplier = Supplier().get_by_id(movement['supplier_id'])
            movement = dict(movement)
            movement['supplier_name'] = supplier['name'] if supplier else ""

        items = self.movement_model.get_movement_details(movement_id)
        company_info = self.settings_model.get_settings()

        filename = f"reports/movement_{movement_id}.pdf"
        self.pdf_gen.generate_invoice(filename, movement, items, company_info)
        return filename

    def get_movement_history(self, **kwargs):
        return self.movement_model.get_history(**kwargs)
