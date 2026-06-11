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
    def has_permission(cls, role_required):
        if not cls._current_user:
            return False

        role = cls._current_user['role']
        if role == 'admin': # المدير العام
            return True

        if role_required == 'supervisor': # المشرف
            return role in ['admin', 'supervisor']

        if role_required == 'warehouse_keeper': # أمين المخزن
            return role in ['admin', 'warehouse_keeper']

        return role == role_required
