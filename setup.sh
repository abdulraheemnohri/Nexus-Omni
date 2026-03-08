#!/bin/bash

# Nexus Omni v5.0 "Horizon" - Automated Installation Script
# Designed for Termux (Android)

set -e

echo "===================================================="
echo "   NEXUS OMNI v5.0 - INSTALLATION STARTED"
echo "===================================================="

# 1. Update Packages
echo "[1/6] Updating Termux packages..."
pkg update && pkg upgrade -y

# 2. Install System Dependencies
echo "[2/6] Installing system dependencies..."
pkg install -y python python-pip clang cmake wget git curl openssl nano nodejs termux-api ffmpeg tesseract ghostscript

# 3. Setup Python Environment
echo "[3/6] Installing Python libraries..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create Project Structure
echo "[4/6] Initializing project structure..."
mkdir -p models data logs modules/templates modules/static backups plugins/automation scripts

# 5. Download Models (Placeholder for User Choice)
echo "[5/6] Model directories prepared. Please download models manually or via dashboard."
# mkdir -p models/vosk-model

# 6. Generate SSL Certificate
echo "[6/6] Generating self-signed SSL certificate..."
if [ ! -f "key.pem" ]; then
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=US/ST=Local/L=Local/O=Nexus/CN=localhost"
    chmod 600 key.pem
    chmod 644 cert.pem
fi

echo "===================================================="
echo "   INSTALLATION COMPLETE!"
echo "===================================================="
echo "Run 'python main.py' to start the brain."
echo "===================================================="
