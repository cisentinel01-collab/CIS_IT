from models.user import User
from models.permission import Permission
from models.audit_log import AuditLog
from utils.auth import AuthManager

class UserController:
    def __init__(self):
        self.user_model = User()
        self.perm_model = Permission()
        self.audit_log = AuditLog()

    def get_all_users(self):
        return self.user_model.get_all_users()

    def add_user(self, data, permissions):
        """
        data: user fields
        permissions: dict {module: {can_view: 1, ...}}
        """
        user_id = self.user_model.create_user(
            data['username'],
            AuthManager.hash_password(data['password']),
            data['full_name'],
            data['role'],
            data.get('job_title'),
            data.get('department')
        )

        for module, perms in permissions.items():
            self.perm_model.set_permission(user_id, module, perms)

        admin = AuthManager.get_current_user()
        self.audit_log.log(admin['id'] if admin else None, "Add User", "users", user_id, f"Created user {data['username']}")
        return user_id

    def update_user(self, user_id, data, permissions=None):
        if 'password' in data and data['password']:
            data['password_hash'] = AuthManager.hash_password(data['password'])
            del data['password']

        self.user_model.update(user_id, data)

        if permissions:
            for module, perms in permissions.items():
                self.perm_model.set_permission(user_id, module, perms)

        admin = AuthManager.get_current_user()
        self.audit_log.log(admin['id'] if admin else None, "Update User", "users", user_id)

    def disable_user(self, user_id):
        self.user_model.update(user_id, {"status": "disabled"})
        admin = AuthManager.get_current_user()
        self.audit_log.log(admin['id'] if admin else None, "Disable User", "users", user_id)

    def get_permissions(self, user_id):
        return self.perm_model.get_user_permissions(user_id)
