#!/bin/bash

# Nexus Omni v4.0 "Ascension" - Automated Installation Script
# Handles deep system dependencies and project initialization

set -e

echo "----------------------------------------------------"
echo "   NEXUS OMNI - INTERNAL MODULE SETUP"
echo "----------------------------------------------------"

# 1. System Packages
echo "[1/5] Installing core system packages..."
# Added libandroid-spawn and pkg-config to fix 'spawn.h' and other build errors
pkg update && pkg upgrade -y
pkg install -y python python-pip clang cmake wget git curl openssl nano nodejs termux-api ffmpeg tesseract ghostscript libandroid-spawn pkg-config

# 2. Python Environment
echo "[2/5] Setting up Python dependencies..."
# Ensure we are in the project root to find requirements.txt
pip install --upgrade pip
# Install numpy separately first as it's a critical dependency
pip install numpy==1.24.0
pip install -r requirements.txt

# 3. Project Directories
echo "[3/5] Initializing data folders..."
mkdir -p models data logs static templates backups scripts

# 4. API Permissions
echo "[4/5] Checking Termux API..."
if command -v termux-battery-status >/dev/null; then
    echo "✓ Termux API is accessible."
else
    echo "! Warning: Termux:API app must be installed from F-Droid for full functionality."
fi

echo "----------------------------------------------------"
echo "   SYSTEM MODULES READY"
echo "----------------------------------------------------"
