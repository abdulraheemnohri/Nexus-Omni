import unittest
import os
import bcrypt
import json
from modules.memory import MemoryManager
from modules.agent import AgentPlanner
from modules.utils import load_config

class TestNexusOmni(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        cls.memory = MemoryManager(cls.config)
        cls.agent = AgentPlanner(cls.config)

    def test_memory_secret_encryption(self):
        key = "test_secret"
        value = "top_secret_123"
        self.memory.store_secret(key, value)
        retrieved = self.memory.get_secret(key)
        self.assertEqual(value, retrieved)

    def test_agent_asimov_layer(self):
        dangerous_cmd = "rm -rf /"
        safe_cmd = "Document this receipt"
        self.assertTrue(self.agent.asimov_check(dangerous_cmd))
        self.assertFalse(self.agent.asimov_check(safe_cmd))

    def test_pin_verification(self):
        pin = "admin"
        stored_hash = self.config['security']['pin_hash']
        self.assertTrue(bcrypt.checkpw(pin.encode(), stored_hash.encode()))
        self.assertFalse(bcrypt.checkpw("wrongpin".encode(), stored_hash.encode()))

    def test_memory_graph_data(self):
        self.memory.add_graph_edge("Mom", "Phone", "has")
        edges = self.memory.get_graph_data()
        self.assertTrue(any(e[0] == "Mom" and e[1] == "Phone" for e in edges))

if __name__ == "__main__":
    unittest.main()
