#!/bin/bash

# Nexus-Omni Termux Installer
# The "One-Liner" entry point for fresh installs

set -e

REPO_URL="https://github.com/abdulraheemnohri/Nexus-Omni.git"
INSTALL_DIR="Nexus-Omni"

echo "----------------------------------------------------"
echo "   NEXUS OMNI v5.0 'HORIZON' INSTALLER"
echo "----------------------------------------------------"
echo "This script will prepare your Termux environment"
echo "and install the Nexus Omni sovereign brain."
echo "----------------------------------------------------"

# 1. Base requirements
echo "[*] Installing git and basic tools..."
pkg update -y
pkg upgrade -y
pkg install -y git openssl

# 2. Clone the repo
if [ -d "$INSTALL_DIR" ]; then
    echo "[!] Directory $INSTALL_DIR already exists. Updating..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "[*] Cloning Nexus Omni..."
    git clone "$REPO_URL"
    cd "$INSTALL_DIR"
fi

# 3. Trigger the internal setup script
echo "[*] Launching system-wide setup..."
chmod +x setup.sh
./setup.sh

echo ""
echo "----------------------------------------------------"
echo "   INSTALLATION SUCCESSFUL!"
echo "----------------------------------------------------"
echo "To start Nexus Brain:"
echo "cd $INSTALL_DIR && python main.py"
echo "----------------------------------------------------"
