class AuthManager:
    _current_user = None

    @classmethod
    def login(cls, username, password):
        from models.user import User
        user = User().authenticate(username, password)
        if user:
            cls._current_user = user
            return True
        return False

    @classmethod
    def get_current_user(cls):
        return cls._current_user

    @classmethod
    def logout(cls):
        cls._current_user = None

    @classmethod
    def has_permission(cls, module, action=None):
        if not cls._current_user:
            return False

        role = cls._current_user['role']
        if role == 'admin':
            return True

        # Warehouse Keeper: Core operations
        if role == 'warehouse_keeper':
            if module in ['items', 'suppliers', 'stock_in', 'stock_out', 'locations', 'dashboard']:
                if action == 'delete':
                    return False
                return True

        # Supervisor: Reports only
        if role == 'supervisor':
            if module in ['reports', 'dashboard']:
                if action in [None, 'view', 'export']:
                    return True

        return False
