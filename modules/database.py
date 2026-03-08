"""
SQLite Database Handler
Tables: memory, todos, notes, chat_history, settings, users
"""

import sqlite3
import datetime
import json
import os

class Database:
    def __init__(self, db_path='data/nexus.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_tables()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        """Create all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Memory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                category TEXT,
                content TEXT,
                importance INTEGER DEFAULT 1,
                embedding BLOB
            )
        ''')

        # Todos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                completed INTEGER DEFAULT 0,
                priority TEXT DEFAULT 'medium',
                due_date TEXT,
                created_at TEXT,
                completed_at TEXT
            )
        ''')

        # Notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                tags TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # Chat history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                message TEXT,
                timestamp TEXT,
                tokens_used INTEGER
            )
        ''')

        # Settings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        ''')

        # Users (for multi-user support)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                pin_hash TEXT,
                created_at TEXT,
                last_login TEXT
            )
        ''')

        # Reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                remind_at TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def save_memory(self, content, category='general'):
        """Save to memory table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO memory (timestamp, category, content) VALUES (?, ?, ?)',
            (datetime.datetime.now().isoformat(), category, content)
        )
        conn.commit()
        conn.close()

    def add_note(self, title, content, tags=''):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO notes (title, content, tags, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
            (title, content, tags, now, now)
        )
        conn.commit()
        conn.close()

    def get_notes(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes ORDER BY updated_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def add_reminder(self, title, remind_at):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reminders (title, remind_at, created_at) VALUES (?, ?, ?)',
            (title, remind_at, datetime.datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def get_reminders(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE is_active = 1 ORDER BY remind_at ASC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def log_security_event(self, event_type, details):
        self.save_memory(f"{event_type}: {details}", category='security')

    def export_all_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        export = {}
        tables = ['memory', 'todos', 'notes', 'chat_history', 'settings']
        for table in tables:
            try:
                cursor.execute(f'SELECT * FROM {table}')
                export[table] = [dict(row) for row in cursor.fetchall()]
            except:
                export[table] = []
        conn.close()
        return export

    def get_memories(self, limit=50, category=None):
        """Retrieve memories"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if category:
            cursor.execute(
                'SELECT * FROM memory WHERE category = ? ORDER BY timestamp DESC LIMIT ?',
                (category, limit)
            )
        else:
            cursor.execute(
                'SELECT * FROM memory ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )

        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def save_setting(self, key, value):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)',
            (key, str(value), datetime.datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def get_setting(self, key, default=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        return row['value'] if row else default

    def add_todo(self, task, priority='medium', due_date=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO todos (task, priority, due_date, created_at) VALUES (?, ?, ?, ?)',
            (task, priority, due_date, datetime.datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def get_todos(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos ORDER BY completed ASC, created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def save_chat(self, role, message):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO chat_history (role, message, timestamp) VALUES (?, ?, ?)',
            (role, message, datetime.datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
