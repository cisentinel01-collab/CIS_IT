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

        # 1. مسئول المخزن (Full Access)
        if role == 'warehouse_manager':
            return True

        # 2. المتابعة (View/Report Only)
        if role == 'follow_up':
            # Allow viewing dashboard and reports
            if module in ['dashboard', 'reports']:
                return True
            # Allow viewing lists (Items, Suppliers, Locations) but no editing
            if module in ['items', 'suppliers', 'locations']:
                return action in [None, 'view', 'export']
            return False

        return False
