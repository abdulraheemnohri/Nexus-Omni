import sqlite3
import os
from cryptography.fernet import Fernet
from modules.utils import get_logger

logger = get_logger("Memory")

class MemoryManager:
    def __init__(self, config):
        self.config = config
        self.db_path = "data/brain_memory.db"
        self.vault_path = "data/vault.db"
        self.key_path = "data/vault.key"
        self._init_dirs()
        self._init_db()
        self._init_vault()

    def _init_dirs(self):
        if not os.path.exists("data"):
            os.makedirs("data")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Semantic memory table
        cursor.execute('''CREATE TABLE IF NOT EXISTS long_term (id INTEGER PRIMARY KEY, content TEXT, embedding BLOB)''')
        # Short term logs
        cursor.execute('''CREATE TABLE IF NOT EXISTS short_term (id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, tag TEXT, content TEXT)''')
        # Knowledge Graph edges
        cursor.execute('''CREATE TABLE IF NOT EXISTS graph_edges (source TEXT, target TEXT, relation TEXT)''')
        conn.commit()
        conn.close()
        logger.info("Memory databases initialized.")

    def _init_vault(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)

        with open(self.key_path, "rb") as key_file:
            self.fernet = Fernet(key_file.read())

        conn = sqlite3.connect(self.vault_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS secrets (key TEXT PRIMARY KEY, encrypted_value BLOB)''')
        conn.commit()
        conn.close()
        logger.info("Encrypted vault initialized.")

    def store_short_term(self, tag, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO short_term (tag, content) VALUES (?, ?)", (tag, content))
        conn.commit()
        conn.close()

    def add_semantic_memory(self, content):
        logger.info(f"Adding semantic memory: {content[:50]}...")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO long_term (content) VALUES (?)", (content,))
        conn.commit()
        conn.close()

    def store_secret(self, key, value):
        encrypted_value = self.fernet.encrypt(value.encode())
        conn = sqlite3.connect(self.vault_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO secrets (key, encrypted_value) VALUES (?, ?)", (key, encrypted_value))
        conn.commit()
        conn.close()

    def get_secret(self, key):
        conn = sqlite3.connect(self.vault_path)
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_value FROM secrets WHERE key=?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return self.fernet.decrypt(row[0]).decode()
        return None

    def add_graph_edge(self, source, target, relation):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO graph_edges (source, target, relation) VALUES (?, ?, ?)", (source, target, relation))
        conn.commit()
        conn.close()

    def get_graph_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT source, target, relation FROM graph_edges")
        edges = cursor.fetchall()
        conn.close()
        return edges
