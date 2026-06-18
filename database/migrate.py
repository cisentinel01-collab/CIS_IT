from models.user import User
from database.db_manager import DBManager

def migrate():
    db = DBManager()
    user_model = User()

    # Responsibilities were consolidated to 2 roles per user request:
    # 1. مسئول المخزن (warehouse_manager) - Full Access
    # 2. المتابعة (follow_up) - View only

    # Check if manager exists
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'warehouse_manager'")
    if res[0]['count'] == 0:
        print("Creating default manager...")
        user_model.create_user({
            "username": "admin",
            "password": "admin",
            "full_name": "مسؤول المخزن",
            "role": "warehouse_manager"
        })

    # Check if follow_up exists
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'follow_up'")
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
