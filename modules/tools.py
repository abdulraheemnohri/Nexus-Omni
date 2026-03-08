"""
Utility Tools Module
"""

import random
import string
import hashlib

def generate_password(length=16, use_special=True):
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|"
    return ''.join(random.choice(chars) for _ in range(length))

def calculate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def format_bytes(size):
    # Convert bytes to human readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:3.1f} {unit}"
        size /= 1024.0
    return f"{size:3.1f} PB"
