#!/data/data/com.termux/files/usr/bin/bash
# Nexus Omni v4.0 - Automated Setup Script

set -e

echo "===================================================="
echo "   NEXUS OMNI v4.0 - INSTALLATION STARTED"
echo "===================================================="

# 1. Update Packages
echo "[1/5] Updating Termux packages..."
pkg update && pkg upgrade -y
# Added libandroid-spawn and pkg-config to fix 'spawn.h' and other build errors
pkg install -y python python-pip clang cmake wget git curl openssl nano nodejs termux-api ffmpeg tesseract ghostscript libandroid-spawn pkg-config

# 2. Python Environment
echo "[2/5] Setting up Python dependencies..."
# Ensure we are in the project root
cd "$(dirname "$0")/.."
pip install --upgrade pip
# Install numpy separately first as it's a critical dependency
pip install numpy==1.24.0
pip install flask flask-cors flask-socketio eventlet psutil cryptography bcrypt

# 3. Optimize Llama-CPP
echo "[3/5] Installing optimized llama-cpp-python..."
CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_METAL=OFF" pip install llama-cpp-python
pip install -r requirements.txt

# 4. Project Directories
echo "[4/5] Initializing data folders..."
mkdir -p modules static templates data/backups data/exports models logs scripts tests

# 5. Whisper (Optional but recommended)
echo "[5/5] Installing OpenAI Whisper..."
pip install openai-whisper

echo "===================================================="
echo "   INSTALLATION COMPLETE!"
echo "===================================================="
echo "Next steps:"
echo "1. Run './scripts/download_model.sh' to get TinyLlama"
echo "2. Run 'python app.py' to start the brain"
echo "===================================================="
