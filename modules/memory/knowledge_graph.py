"""
Knowledge Graph for v5.0
Maps relationships between entities in memory
"""

class KnowledgeGraph:
    def __init__(self, db):
        self.db = db

    def add_relationship(self, subject, predicate, object_entity):
        """Save a triple to a graph-like structure (stored in SQLite)"""
        # conn = self.db.get_connection()
        # cursor.execute('INSERT INTO knowledge_graph ...')
        pass

    def query_relationships(self, entity):
        """Find everything related to an entity"""
        return []
