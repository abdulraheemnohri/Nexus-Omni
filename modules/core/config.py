"""
Configuration Manager for Nexus Omni v5.0
"""

import json
import os

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return self.get_default_config()
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get_default_config(self):
        return {
            "app": {
                "name": "Nexus Omni",
                "version": "5.0",
                "debug": False,
                "host": "127.0.0.1",
                "port": 5000,
                "secret_key": os.urandom(24).hex()
            },
            "ai": {
                "primary_model": "tinyllama",
                "fallback_model": "rules",
                "context_window": 2048,
                "max_tokens": 512,
                "temperature": 0.7,
                "threads": 4
            },
            "database": {
                "path": "data/nexus.db",
                "encryption_enabled": True
            },
            "security": {
                "pin_enabled": True,
                "session_timeout": 900
            }
        }

    def get(self, key, default=None):
        parts = key.split('.')
        data = self.config
        for part in parts:
            if isinstance(data, dict):
                data = data.get(part)
            else:
                return default
        return data if data is not None else default

    def save(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
