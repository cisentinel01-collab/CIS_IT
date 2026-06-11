import shutil
import datetime
import os

class BackupManager:
    def __init__(self, db_path="database/wms.db", backup_dir="backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"wms_backup_{timestamp}.db")
        try:
            shutil.copy2(self.db_path, backup_file)
            return backup_file
        except Exception as e:
            print(f"Backup error: {e}")
            return None

    def restore_backup(self, backup_file):
        try:
            shutil.copy2(backup_file, self.db_path)
            return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False

    def list_backups(self):
        return sorted([f for f in os.listdir(self.backup_dir) if f.endswith(".db")], reverse=True)
