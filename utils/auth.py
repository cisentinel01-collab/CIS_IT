import bcrypt

class AuthManager:
    _current_user = None

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @classmethod
    def set_current_user(cls, user):
        cls._current_user = user

    @classmethod
    def get_current_user(cls):
        return cls._current_user

    @classmethod
    def logout(cls):
        cls._current_user = None

    @classmethod
    def has_permission(cls, module_name, action=None):
        """
        Checks if the current user has permission for a specific module and action.
        """
        if not cls._current_user:
            return False

        role = cls._current_user.get('role', '')
        if role == 'admin':
            return True

        if action:
            try:
                from models.permission import Permission
                return Permission().has_permission(cls._current_user['id'], module_name, action)
            except Exception as e:
                print(f"Permission check error: {e}")
                return False

        # Default role-based fallbacks if no specific action provided
        if module_name == 'supervisor':
            return role in ['admin', 'supervisor']
        if module_name == 'warehouse_keeper':
            return role in ['admin', 'warehouse_keeper']

        return True
