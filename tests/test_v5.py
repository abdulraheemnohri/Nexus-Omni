"""
Core Tests for Nexus Omni v5.0
"""
import pytest
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.core.config import ConfigManager
from modules.database.sqlite_handler import DatabaseManager
from modules.security.auth import hash_pin, verify_pin
from modules.ai.engine import AIEngine

def test_config_loading(tmp_path):
    config_file = tmp_path / "config.json"
    cfg = ConfigManager(str(config_file))
    assert cfg.get("app.name") == "Nexus Omni"
    assert cfg.get("app.version") == "5.0"

def test_database_init(tmp_path):
    db_file = tmp_path / "nexus.db"
    db = DatabaseManager(str(db_file))
    assert os.path.exists(str(db_file))

    # Test User
    db.add_user("testuser", "hashed_pin")
    user = db.get_user("testuser")
    assert user['username'] == "testuser"

def test_auth():
    pin = "1234"
    hashed = hash_pin(pin)
    assert verify_pin(pin, hashed) is True
    assert verify_pin("wrong", hashed) is False

def test_ai_safety(tmp_path):
    db_file = tmp_path / "test_ai.db"
    db = DatabaseManager(str(db_file))
    cfg = ConfigManager("non_existent.json")
    ai = AIEngine(cfg, db)

    # Test dangerous command
    result = ai.process(1, "rm -rf /")
    assert "sensitive" in result['response']
    assert result['source'] == "safety_layer"

def test_ai_rules(tmp_path):
    db_file = tmp_path / "test_rules.db"
    db = DatabaseManager(str(db_file))
    cfg = ConfigManager("non_existent.json")
    ai = AIEngine(cfg, db)

    result = ai.process(1, "What time is it?")
    assert "currently" in result['response']
    assert result['source'] == "rules"
