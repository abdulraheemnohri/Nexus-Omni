"""
Nexus Omni Constants
"""

import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
PLUGINS_DIR = os.path.join(BASE_DIR, 'modules', 'plugins')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Database
DB_PATH = os.path.join(DATA_DIR, 'nexus.db')

# Security
PIN_HASH_KEY = 'pin_hash'

# AI
DEFAULT_MODEL = 'tinyllama'
