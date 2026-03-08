"""
Encryption utilities for v5.0
Uses Fernet for symmetric encryption
"""

from cryptography.fernet import Fernet
import base64
import os

class EncryptionManager:
    def __init__(self, key=None):
        if key:
            self.key = key
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()

    def decrypt(self, token):
        return self.cipher.decrypt(token.encode()).decode()

    def get_key(self):
        return self.key.decode()
