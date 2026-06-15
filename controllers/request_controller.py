from models.purchase_request import PurchaseRequest
from models.audit_log import AuditLog
from utils.auth import AuthManager
import datetime

class RequestController:
    def __init__(self):
        self.request_model = PurchaseRequest()
        self.audit_log = AuditLog()

    def create_request(self, data, items):
        if 'request_no' not in data:
            data['request_no'] = f"REQ-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        request_id = self.request_model.create_request(data, items)

        user = AuthManager.get_current_user()
        self.audit_log.log(user['id'] if user else None, "Create Purchase Request", "purchase_requests", request_id)
        return request_id

    def approve_request(self, request_id):
        user = AuthManager.get_current_user()
        self.request_model.update_status(request_id, "approved", approved_by=user['id'])
        self.audit_log.log(user['id'], "Approve Request", "purchase_requests", request_id)

    def reject_request(self, request_id, reason):
        user = AuthManager.get_current_user()
        self.request_model.update_status(request_id, "rejected", reason=reason)
        self.audit_log.log(user['id'], "Reject Request", "purchase_requests", request_id)

    def get_all_requests(self, status=None):
        return self.request_model.get_all_requests(status)

    def get_details(self, request_id):
        return self.request_model.get_request_details(request_id)
