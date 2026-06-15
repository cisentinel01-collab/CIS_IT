from models.base_model import BaseModel

class AuditLog(BaseModel):
    table_name = "audit_logs"

    def log(self, user_id, action, table_name=None, record_id=None, details=None, old_value=None, new_value=None, device_name=None, ip_address=None):
        self.create({
            "user_id": user_id,
            "action": action,
            "table_name": table_name,
            "record_id": record_id,
            "details": details,
            "old_value": str(old_value) if old_value is not None else None,
            "new_value": str(new_value) if new_value is not None else None,
            "device_name": device_name,
            "ip_address": ip_address
        })

    def get_logs(self, limit=100):
        query = """
            SELECT al.*, u.username
            FROM audit_logs al
            LEFT JOIN users u ON al.user_id = u.id
            ORDER BY al.timestamp DESC
            LIMIT ?
        """
        return self.db.execute_query(query, (limit,))
