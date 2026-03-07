# Nexus Omni v5.0 "Horizon"
## The Ultimate Offline Sovereign Mobile Brain

Nexus Omni is a fully offline, privacy-centric, autonomous AI agent for Android. It integrates Voice, Vision, System Control, Semantic Memory, and Agentic Planning without any cloud dependency.

---

## 🚀 Installation Guide

### 1. Termux Preparation
Install **Termux** from F-Droid (not Play Store). Open Termux and run:
```bash
# Grant Storage Permission
termux-setup-storage

# Update & Install Base Packages
pkg update && pkg upgrade
pkg install python python-pip clang cmake ffmpeg wget ghostscript tesseract openssl git nodejs termux-api
```

### 2. Dependency Installation
Clone this repository and install the Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Model Deployment
Nexus requires local models for STT, LLM, and Vision:
```bash
mkdir -p models

# 1. Speech Model (Vosk)
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d models/

# 2. LLM Model (TinyLlama GGUF)
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
mv tinyllama*.gguf models/llm.gguf

# 3. Vision Model (YOLO Nano)
# Download yolo.tflite and place in models/
```

### 4. SSL Certificate Generation
To access the Dashboard securely via HTTPS:
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

---

## ⚙️ Setup Guide

### 1. ADB Wireless Configuration (Android 11+)
1.  **Enable Developer Options:** Settings > About Phone > Tap Build Number 7x.
2.  **Enable Wireless Debugging:** Developer Options > Wireless Debugging.
3.  **Pair Device:** Note the IP, Port, and Pairing Code.
4.  **Connect in Termux:**
    ```bash
    adb pair [IP:PORT] [CODE]
    adb connect [IP:PORT]
    ```

### 2. Tasker Bridge (Optional for Deep Control)
1. Install **Tasker**.
2. Create Profile: **Event > Intent Received > Action: `com.nexus.COMMAND`**.
3. Grant Tasker **Accessibility Service** permission.

### 3. Launching Nexus
Run the orchestrator:
```bash
python3 main.py
```

### 4. Accessing the Dashboard
1. Open your mobile browser.
2. Navigate to `https://127.0.0.1:5000`.
3. Accept the self-signed certificate warning.
4. Login with the default PIN (Set in `config.json`).

---

## 🛠 Features
- **Full-Stack Dashboard:** Real-time monitoring and control.
- **Agentic Planning:** Goal decomposition via Local LLM.
- **Semantic Memory:** Long-term factual recall using Vector DB.
- **Knowledge Graph:** Visual relationship mapping between entities.
- **Energy Aware:** Automatic model switching based on battery status.
- **Kill Switch:** Immediate emergency lockdown protocols.

---

## 🛡 Security & Privacy
- **Zero Cloud:** All processing happens on-device.
- **Encryption:** Databases and secrets are encrypted with device-unique keys.
- **Asimov Layer:** Hardcoded safety restrictions prevent harmful system commands.

*Build Nexus Omni. Visualize the Mind. Secure the Future. Own Your Data.*
