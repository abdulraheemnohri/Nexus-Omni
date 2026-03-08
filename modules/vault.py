"""
Encrypted Vault Module
"""

from modules.security import Security
import sqlite3
import os

class Vault:
    def __init__(self, config):
        self.config = config
        self.security = Security(config)
        self.db_path = 'data/vault.db'
        self._init_db()

    def _init_db(self):
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("CREATE TABLE IF NOT EXISTS secrets (key TEXT PRIMARY KEY, value BLOB)")
        conn.commit()
        conn.close()

    def store_secret(self, key, value):
        encrypted = self.security.encrypt(value)
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT OR REPLACE INTO secrets (key, value) VALUES (?, ?)", (key, encrypted))
        conn.commit()
        conn.close()

    def get_secret(self, key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM secrets WHERE key=?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return self.security.decrypt(row[0])
        return None
