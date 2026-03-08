"""
Database Backup Manager for v5.0
"""
import shutil
import os
import datetime

class BackupManager:
    def __init__(self, db_path, backup_dir):
        self.db_path = db_path
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        dest = os.path.join(self.backup_dir, f'nexus_backup_{timestamp}.db')
        try:
            shutil.copy2(self.db_path, dest)
            return dest
        except Exception as e:
            print(f"Backup failed: {e}")
            return None

    def list_backups(self):
        return sorted(os.listdir(self.backup_dir), reverse=True)
