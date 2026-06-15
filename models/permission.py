from models.base_model import BaseModel

class Permission(BaseModel):
    table_name = "permissions"

    def get_user_permissions(self, user_id):
        query = f"SELECT * FROM {self.table_name} WHERE user_id = ?"
        results = self.db.execute_query(query, (user_id,))
        return {r['module']: r for r in results}

    def set_permission(self, user_id, module, perms):
        """
        perms: dict with can_view, can_add, etc.
        """
        existing = self.db.execute_query(f"SELECT id FROM {self.table_name} WHERE user_id = ? AND module = ?", (user_id, module))
        if existing:
            self.update(existing[0]['id'], perms)
        else:
            data = {"user_id": user_id, "module": module}
            data.update(perms)
            self.create(data)

    def has_permission(self, user_id, module, action):
        query = f"SELECT {action} FROM {self.table_name} WHERE user_id = ? AND module = ?"
        results = self.db.execute_query(query, (user_id, module))
        if results and results[0][action] == 1:
            return True
        return False
