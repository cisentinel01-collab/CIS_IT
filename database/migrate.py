from models.user import User
from database.db_manager import DBManager

def migrate():
    db = DBManager()
    user_model = User()

    # Responsibilities were consolidated to 2 roles per user request:
    # 1. مسؤول المخزن (warehouse_manager) - Full Access
    # 2. المتابعة (follow_up) - View only

    # Check if manager exists
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
    if res[0]['count'] == 0:
        print("Creating default manager...")
        user_model.create_user({
            "username": "admin",
            "password": "admin",
            "full_name": "مسؤول المخزن",
            "role": "warehouse_manager"
        })
    else:
        print("Updating existing admin to manager role...")
        db.execute_query("UPDATE users SET role = 'warehouse_manager', full_name = 'مسؤول المخزن' WHERE username = 'admin'", commit=True)

    # Check if follow_up exists
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE username = 'user'")
    if res[0]['count'] == 0:
        print("Creating default follow-up user...")
        user_model.create_user({
            "username": "user",
            "password": "user",
            "full_name": "المتابعة",
            "role": "follow_up"
        })

    print("Migration complete.")

if __name__ == "__main__":
    migrate()
