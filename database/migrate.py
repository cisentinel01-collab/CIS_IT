import sqlite3
import os

def migrate():
    db_path = "database/wms.db"
    migrate_path = "database/migrate_v2.sql"

    if not os.path.exists(db_path):
        print("Database not found. Initializing with schema.sql first...")
        # (Assuming main.py or db_manager will handle initial setup)
        return

    with open(migrate_path, "r", encoding="utf-8") as f:
        migrate_script = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Split by semicolon but ignore inside strings if possible.
    # For simple migration scripts, splitting by ';' is usually enough.
    statements = migrate_script.split(';')

    for statement in statements:
        if statement.strip():
            try:
                cursor.execute(statement)
            except sqlite3.OperationalError as e:
                # Ignore "duplicate column name" errors during migration re-runs
                if "duplicate column name" in str(e).lower():
                    pass
                else:
                    print(f"Error executing statement: {e}")
                    print(f"Statement: {statement}")

    conn.commit()
    conn.close()
    print("Migration V2 completed.")

if __name__ == "__main__":
    migrate()
