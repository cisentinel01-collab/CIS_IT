import shutil
import os
import datetime

class BackupManager:
    @staticmethod
    def create_backup(db_path="database/wms_v2.db", backup_dir="backups"):
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")
        shutil.copy2(db_path, backup_path)
        return backup_path

    @staticmethod
    def restore_backup(backup_path, db_path="database/wms_v2.db"):
        shutil.copy2(backup_path, db_path)
        return True
