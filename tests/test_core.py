import unittest
import os
import json
from modules.database import Database
from modules.ai_engine import AIEngine
from modules.security import Security

class TestNexusOmniV4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('config.json', 'r') as f:
            cls.config = json.load(f)
        cls.db = Database(cls.config['database']['path'])
        cls.engine = AIEngine(cls.config)
        cls.security = Security(cls.config)

    def test_database_persistence(self):
        self.db.save_setting('test_key', 'test_value')
        self.assertEqual(self.db.get_setting('test_key'), 'test_value')

    def test_security_hashing(self):
        pin = "1234"
        hashed = self.security.hash_pin(pin)
        self.assertTrue(self.security.verify_pin(pin, hashed))

    def test_engine_rules(self):
        response = self.engine.process("what time is it")
        self.assertIn("The current time is", response['response'])

if __name__ == "__main__":
    unittest.main()
