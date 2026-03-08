#!/data/data/com.termux/files/usr/bin/bash
# Nexus Omni - Installation Script for Termux

echo "🚀 Starting Nexus Omni v4.0 Installation..."

# 1. System Packages
pkg update && pkg upgrade -y
pkg install python python-pip clang cmake wget git ffmpeg nano termux-api -y

# 2. Python Dependencies
CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_METAL=OFF" pip install llama-cpp-python
pip install -r requirements.txt

# 3. Directories
mkdir -p data/backups data/exports models logs scripts modules templates static

echo "✅ Installation Complete! Run ./scripts/download_model.sh to get the AI model."
