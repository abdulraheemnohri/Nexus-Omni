"""
Backup & Restore Module
"""

import shutil
import os
import datetime

class BackupManager:
    def __init__(self, config):
        self.config = config
        self.data_dir = 'data'
        self.backup_dir = config['database']['backup_location']

    def create_backup(self):
        os.makedirs(self.backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(self.backup_dir, f"nexus_backup_{timestamp}.zip")
        shutil.make_archive(backup_path.replace('.zip', ''), 'zip', self.data_dir)
        return backup_path
