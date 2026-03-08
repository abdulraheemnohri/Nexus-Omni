#!/usr/bin/env python3
"""
Secure Vault Module
"""

import os
import sqlite3
from cryptography.fernet import Fernet

class SecureVault:
    def __init__(self, config):
        self.config = config
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'vault.db')
        self.key_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'vault.key')
        self._init_vault()

    def _init_vault(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(key)

        with open(self.key_path, "rb") as f:
            self.fernet = Fernet(f.read())

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS secrets (key TEXT PRIMARY KEY, value BLOB)")
        self.conn.commit()

    def store(self, key, value):
        encrypted = self.fernet.encrypt(value.encode())
        self.cursor.execute("INSERT OR REPLACE INTO secrets (key, value) VALUES (?, ?)", (key, encrypted))
        self.conn.commit()

    def get(self, key):
        self.cursor.execute("SELECT value FROM secrets WHERE key=?", (key,))
        row = self.cursor.fetchone()
        if row:
            return self.fernet.decrypt(row[0]).decode()
        return None

    def close(self):
        self.conn.close()
