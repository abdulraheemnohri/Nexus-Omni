"""
Security Authentication Utilities
"""
import bcrypt

def hash_pin(pin):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pin.encode(), salt).decode()

def verify_pin(pin, hashed):
    return bcrypt.checkpw(pin.encode(), hashed.encode())
