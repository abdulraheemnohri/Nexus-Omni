import unittest
import os
import bcrypt
import json
from modules.memory import BrainMemory
from modules.agent import AgentPlanner
from modules.utils import load_config
from modules.control import ADBController

class TestNexusOmni(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        cls.memory = BrainMemory(cls.config)
        cls.controller = ADBController(cls.config['network']['adb_ip'])
        cls.agent = AgentPlanner(cls.config, cls.controller, cls.memory)

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
