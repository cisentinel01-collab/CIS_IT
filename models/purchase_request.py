from models.base_model import BaseModel

class PurchaseRequest(BaseModel):
    table_name = "purchase_requests"

    def create_request(self, request_data, items_list):
        request_id = self.create(request_data)
        for item in items_list:
            query = "INSERT INTO request_items (request_id, item_id, quantity) VALUES (?, ?, ?)"
            self.db.execute_query(query, (request_id, item['item_id'], item['quantity']), commit=True)
        return request_id

    def get_request_details(self, request_id):
        query = """
            SELECT ri.*, i.name as item_name, i.code as item_code, i.unit
            FROM request_items ri
            JOIN items i ON ri.item_id = i.id
            WHERE ri.request_id = ?
        """
        return self.db.execute_query(query, (request_id,))

    def update_status(self, request_id, status, approved_by=None, reason=None):
        data = {"status": status}
        if approved_by: data["approved_by"] = approved_by
        if reason: data["rejection_reason"] = reason
        self.update(request_id, data)

    def get_all_requests(self, status=None):
        query = f"SELECT * FROM {self.table_name} WHERE is_deleted = 0"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY date DESC"
        return self.db.execute_query(query, tuple(params))
