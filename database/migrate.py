from models.user import User
from database.db_manager import DBManager

def migrate():
    db = DBManager()
    user_model = User()

    # Requirements:
    # 1. Admin (Full access + User Management) - pass: adminyousef
    # 2. مسؤول المخزن (Full access except Users)
    # 3. المتابعة (View only)

    # Check if any admin exists. If not, create the default one.
    # We NO LONGER delete users here to preserve data added via UI.

    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'admin'")
    if res[0]['count'] == 0:
        print("Creating default admin...")
        user_model.create_user({
            "username": "admin",
            "password": "adminyousef",
            "full_name": "المدير العام",
            "role": "admin"
        })

    # Check for warehouse_manager
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'warehouse_manager'")
    if res[0]['count'] == 0:
        print("Creating default manager...")
        user_model.create_user({
            "username": "manager",
            "password": "123",
            "full_name": "مسؤول المخزن",
            "role": "warehouse_manager"
        })

    # Check for follow_up
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'follow_up'")
    if res[0]['count'] == 0:
        print("Creating default follow-up user...")
        user_model.create_user({
            "username": "user",
            "password": "123",
            "full_name": "المتابعة",
            "role": "follow_up"
        })

    print("Migration complete. System ready.")

if __name__ == "__main__":
    migrate()
