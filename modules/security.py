"""
Security & Encryption Module
Features: PIN Auth, Data Encryption, Session Management
"""

import bcrypt
import hashlib
from cryptography.fernet import Fernet
import os

class Security:
    def __init__(self, config):
        self.encryption_enabled = config['security']['encryption_enabled']
        self.key_file = 'data/.encryption_key'
        self.key = self.load_or_create_key()
        self.cipher = Fernet(self.key) if self.encryption_enabled else None

    def load_or_create_key(self):
        """Load or generate encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs('data', exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # os.chmod(self.key_file, 0o600)  # Secure permissions - might fail on some platforms
            return key

    def hash_pin(self, pin):
        """Hash PIN for storage"""
        return bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()

    def verify_pin(self, pin, hashed):
        """Verify PIN against hash"""
        if not hashed: return False
        return bcrypt.checkpw(pin.encode(), hashed.encode())

    def encrypt(self, data):
        """Encrypt sensitive data"""
        if not self.encryption_enabled or not self.cipher:
            return data
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, data):
        """Decrypt sensitive data"""
        if not self.encryption_enabled or not self.cipher:
            return data
        return self.cipher.decrypt(data.encode()).decode()
