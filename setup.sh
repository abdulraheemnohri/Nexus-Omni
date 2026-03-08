#!/bin/bash

# Nexus Omni v5.0 "Horizon" - Internal Setup Script
# Handles deep system dependencies and project initialization

set -e

echo "----------------------------------------------------"
echo "   NEXUS OMNI - INTERNAL MODULE SETUP"
echo "----------------------------------------------------"

# 1. System Packages
echo "[1/5] Installing core system packages..."
pkg install -y python python-pip clang cmake wget curl nano nodejs termux-api ffmpeg tesseract ghostscript proot proot-distro libjpeg-turbo libpng

# 2. Python Environment
echo "[2/5] Setting up Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Project Directories
echo "[3/5] Initializing data folders..."
mkdir -p models data logs modules/templates modules/static backups plugins/automation scripts

# 4. SSL Generation
echo "[4/5] Generating dashboard security certificates..."
if [ ! -f "key.pem" ]; then
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=US/ST=Local/L=Local/O=Nexus/CN=localhost"
    chmod 600 key.pem
    chmod 644 cert.pem
    echo "✓ Certificates generated."
else
    echo "✓ Certificates already exist."
fi

# 5. API Permissions
echo "[5/5] Checking Termux API..."
if command -v termux-battery-status >/dev/null; then
    echo "✓ Termux API is accessible."
else
    echo "! Warning: Termux:API app must be installed from F-Droid for full functionality."
fi

echo "----------------------------------------------------"
echo "   SYSTEM MODULES READY"
echo "----------------------------------------------------"
