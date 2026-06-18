from models.user import User
from database.db_manager import DBManager

def migrate():
    db = DBManager()
    user_model = User()

    # Check if admin exists
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'admin'")
    if res[0]['count'] == 0:
        print("Creating default admin...")
        user_model.create_user({
            "username": "admin",
            "password": "admin",
            "full_name": "المدير العام",
            "role": "admin"
        })

    # Check if keeper exists
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'warehouse_keeper'")
    if res[0]['count'] == 0:
        print("Creating default warehouse keeper...")
        user_model.create_user({
            "username": "keeper",
            "password": "keeper",
            "full_name": "أمين المخزن",
            "role": "warehouse_keeper"
        })

    # Check if supervisor exists
    res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'supervisor'")
    if res[0]['count'] == 0:
        print("Creating default supervisor...")
        user_model.create_user({
            "username": "supervisor",
            "password": "supervisor",
            "full_name": "المشرف",
            "role": "supervisor"
        })

    print("Migration complete.")

if __name__ == "__main__":
    migrate()
