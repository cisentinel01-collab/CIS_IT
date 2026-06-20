from models.base_model import BaseModel
import bcrypt

class User(BaseModel):
    table_name = "users"

    def authenticate(self, username, password):
        query = "SELECT * FROM users WHERE username =  %s  AND is_active = 1"
        results = self.db.execute_query(query, (username,))
        if results:
            user = results[0]
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                return user
        return None

    def create_user(self, data):
        if 'password' in data:
            data['password_hash'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            del data['password']
        return self.create(data)

    def get_all(self):
        # Users don't have is_deleted usually, but status
        query = "SELECT * FROM users"
        return self.db.execute_query(query)
