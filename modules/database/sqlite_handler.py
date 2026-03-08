"""
Advanced SQLite Handler for Nexus Omni v5.0
"""

import sqlite3
import os
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pin_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT,
            settings TEXT,
            status TEXT DEFAULT 'active'
        )''')

        # Chat History
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            tokens_used INTEGER,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')

        # Memory Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT,
            content TEXT NOT NULL,
            importance INTEGER DEFAULT 1,
            embedding BLOB,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')

        # Todos Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'medium',
            due_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')

        # Notes Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT NOT NULL,
            tags TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')

        # Settings Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')

        # Automation Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS automation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            trigger_type TEXT,
            trigger_config TEXT,
            action_type TEXT,
            action_config TEXT,
            enabled INTEGER DEFAULT 1,
            last_run TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')

        # Logs Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT,
            module TEXT,
            message TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )''')

        # Create Indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_history(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_timestamp ON chat_history(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_memory_user ON memory(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_memory_category ON memory(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_todos_user ON todos(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed)')

        conn.commit()
        conn.close()

    # --- User Methods ---
    def add_user(self, username, pin_hash):
        conn = self.get_connection()
        try:
            conn.execute('INSERT INTO users (username, pin_hash) VALUES (?, ?)', (username, pin_hash))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user(self, username):
        conn = self.get_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return user

    # --- Chat Methods ---
    def save_chat(self, user_id, role, message, tokens=0):
        conn = self.get_connection()
        conn.execute('INSERT INTO chat_history (user_id, role, message, tokens_used) VALUES (?, ?, ?, ?)',
                    (user_id, role, message, tokens))
        conn.commit()
        conn.close()

    def get_chat_history(self, user_id, limit=50):
        conn = self.get_connection()
        history = conn.execute('SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
                              (user_id, limit)).fetchall()
        conn.close()
        return [dict(row) for row in reversed(history)]

    # --- Todo Methods ---
    def add_todo(self, user_id, task, priority='medium', due_date=None):
        conn = self.get_connection()
        conn.execute('INSERT INTO todos (user_id, task, priority, due_date) VALUES (?, ?, ?, ?)',
                    (user_id, task, priority, due_date))
        conn.commit()
        conn.close()

    def get_todos(self, user_id, completed=0):
        conn = self.get_connection()
        todos = conn.execute('SELECT * FROM todos WHERE user_id = ? AND completed = ? ORDER BY created_at DESC',
                            (user_id, completed)).fetchall()
        conn.close()
        return [dict(row) for row in todos]

    # --- Settings Methods ---
    def save_setting(self, user_id, key, value):
        conn = self.get_connection()
        conn.execute('''INSERT INTO settings (user_id, key, value) VALUES (?, ?, ?)
                        ON CONFLICT(id) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP''',
                    (user_id, key, value))
        conn.commit()
        conn.close()

    def get_setting(self, user_id, key, default=None):
        conn = self.get_connection()
        row = conn.execute('SELECT value FROM settings WHERE user_id = ? AND key = ?', (user_id, key)).fetchone()
        conn.close()
        return row['value'] if row else default
