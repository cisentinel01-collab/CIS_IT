from models.base_model import BaseModel

class User(BaseModel):
    table_name = "users"

    def get_by_username(self, username):
        query = f"SELECT * FROM {self.table_name} WHERE username = ? AND is_active = 1"
        results = self.db.execute_query(query, (username,))
        return results[0] if results else None

    def create_user(self, username, password_hash, full_name, role):
        return self.create({
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
            "role": role
        })
