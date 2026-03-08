"""
Semantic Memory Module
"""

from modules.database import Database

class MemoryManager:
    def __init__(self, config):
        self.config = config
        self.db = Database(config['database']['path'])

    def add_memory(self, content, category='general'):
        return self.db.save_memory(content, category)

    def search_memories(self, query, limit=10):
        return self.db.get_memories(limit=limit)
