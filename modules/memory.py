#!/usr/bin/env python3
"""
Memory Module - SQLite + Vector Embeddings
"""

import os
import sqlite3
import datetime
import json
try:
    import sqlite_vec
except ImportError:
    sqlite_vec = None

class BrainMemory:
    def __init__(self, config):
        self.config = config
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'brain_memory.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        if sqlite_vec:
            self.conn.enable_load_extension(True)
            sqlite_vec.load(self.conn)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        # Standard memory table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                category TEXT,
                content TEXT,
                importance INTEGER DEFAULT 1
            )
        ''')

        # Knowledge Graph edges
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS graph_edges (
                source TEXT,
                target TEXT,
                relation TEXT
            )
        ''')

        # Vector memory table for semantic search (if sqlite-vec available)
        if sqlite_vec:
            self.cursor.execute('''
                CREATE VIRTUAL TABLE IF NOT EXISTS semantic_memory USING vec0(
                    embedding float[384],
                    content TEXT,
                    timestamp TEXT,
                    category TEXT
                )
            ''')

        self.conn.commit()

    def save(self, content, category="general", importance=1):
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute(
            "INSERT INTO memory (timestamp, category, content, importance) VALUES (?, ?, ?, ?)",
            (timestamp, category, content, importance)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def add_graph_edge(self, source, target, relation):
        self.cursor.execute(
            "INSERT INTO graph_edges (source, target, relation) VALUES (?, ?, ?)",
            (source, target, relation)
        )
        self.conn.commit()

    def get_graph_data(self):
        self.cursor.execute("SELECT source, target, relation FROM graph_edges")
        return self.cursor.fetchall()

    def search(self, query, limit=5):
        self.cursor.execute(
            "SELECT content, timestamp FROM memory WHERE content LIKE ? ORDER BY timestamp DESC LIMIT ?",
            (f"%{query}%", limit)
        )
        return self.cursor.fetchall()

    def get_recent(self, limit=10):
        self.cursor.execute(
            "SELECT content, timestamp, category FROM memory ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
