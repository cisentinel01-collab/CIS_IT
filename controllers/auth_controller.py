from models.user import User
from models.audit_log import AuditLog
from utils.auth import AuthManager

class AuthController:
    def __init__(self):
        self.user_model = User()
        self.audit_log = AuditLog()

    def login(self, username, password):
        user = self.user_model.get_by_username(username)
        if user and AuthManager.verify_password(password, user['password_hash']):
            AuthManager.set_current_user(user)
            self.audit_log.log(user['id'], "Login", details=f"User {username} logged in")
            return True, user
        return False, None

    def logout(self):
        user = AuthManager.get_current_user()
        if user:
            self.audit_log.log(user['id'], "Logout")
            AuthManager.logout()
