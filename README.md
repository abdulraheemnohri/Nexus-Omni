# 📘 NEXUS OMNI v5.0 "HORIZON"
## Complete Installation & Setup Guide for Termux (Android)

**The Ultimate Offline Sovereign Mobile Brain with Full-Stack Dashboard**

---

## 📋 TABLE OF CONTENTS

1. [Prerequisites & Warnings](#1-prerequisites--warnings)
2. [Termux Installation & Base Setup](#2-termux-installation--base-setup)
3. [Project Directory Structure](#3-project-directory-structure)
4. [Package & Library Installation](#4-package--library-installation)
5. [AI Model Downloads](#5-ai-model-downloads)
6. [SSL Certificate Generation](#6-ssl-certificate-generation)
7. [Configuration Files](#7-configuration-files)
8. [Core Module Code](#8-core-module-code)
9. [Dashboard Setup](#9-dashboard-setup)
10. [ADB Wireless Configuration](#10-ADB-wireless-configuration)
11. [Tasker Bridge Setup](#11-tasker-bridge-setup)
12. [Boot Automation](#12-boot-automation)
13. [First Launch & Testing](#13-first-launch--testing)
14. [Security Hardening](#14-security-hardening)
15. [Troubleshooting Guide](#15-troubleshooting-guide)

---

## 1. PREREQUISITES & WARNINGS ⚠️

### Hardware Requirements
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Android Version** | 11+ | 13+ |
| **RAM** | 6GB | 8GB+ |
| **Storage** | 10GB Free | 20GB+ Free |
| **Battery** | 4000mAh | 5000mAh+ |
| **Processor** | Snapdragon 730+ | Snapdragon 865+ |

### ⚠️ CRITICAL WARNINGS
1. **DO NOT** install Termux from Google Play Store (outdated). Use **F-Droid** only.
2. **Backup your data** before starting. This project modifies system settings.
3. **Battery drain is expected**. AI processes are energy-intensive.
4. **ADB Wireless** must be re-paired after every reboot.
5. **Never expose Dashboard to public internet**. Localhost only unless you understand SSL/security.

### Required Apps (Install Before Starting)
| App | Source | Purpose |
|-----|--------|---------|
| **Termux** | F-Droid | Main environment |
| **Termux:API** | F-Droid | Sensor/Hardware access |
| **Termux:Boot** | F-Droid | Auto-start on boot |
| **Termux:Widget** | F-Droid | Quick launch shortcuts |
| **Tasker** | Play Store | Accessibility bridge (Paid) |
| **MacroDroid** | Play Store | Free Tasker alternative |

---

## 2. TERMUX INSTALLATION & BASE SETUP

### Step 2.1: Install Termux from F-Droid
```bash
# 1. Download F-Droid from https://f-droid.org
# 2. Open F-Droid and search "Termux"
# 3. Install "Termux" (by Fredrik Fornwall)
# 4. Install "Termux:API", "Termux:Boot", "Termux:Widget"
```

### Step 2.2: Initial Termux Setup
```bash
# Open Termux and run these commands ONE BY ONE

# Grant storage permission
termux-setup-storage

# Update package lists
pkg update

# Upgrade all packages
pkg upgrade -y

# Install essential build tools
pkg install -y python python-pip clang cmake wget git curl openssl nano vim

# Install Termux API package
pkg install -y termux-api

# Grant Android permissions (Run in Termux, then check Android Settings)
termux-setup-storage
```

---

## 3. PROJECT DIRECTORY STRUCTURE

### Expected Structure:
```
/home/termux/nexus_omni/
├── main.py
├── config.json
├── requirements.txt
├── modules/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── agent.py
│   ├── memory.py
│   ├── voice.py
│   ├── control.py
│   ├── vision.py
│   ├── sensors.py
│   ├── vault.py
│   ├── autopilot.py
│   └── plugin_engine.py
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── console.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── models/
│   ├── vosk-model/
│   ├── llm.gguf
│   └── yolo.tflite
├── data/
│   ├── brain_memory.db
│   ├── semantic_memory.db
│   └── vault.db
├── logs/
│   └── nexus.log
├── plugins/
├── backups/
├── scripts/
│   ├── start_brain.sh
│   ├── stop_brain.sh
│   └── reconnect_adb.sh
├── cert.pem
└── key.pem
```

---

## 4. PACKAGE & LIBRARY INSTALLATION

### Step 4.1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## 5. AI MODEL DOWNLOADS

### Step 5.1: Download Vosk Speech Model (40MB)
```bash
cd ~/nexus_omni/models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 vosk-model
rm vosk-model-small-en-us-0.15.zip
```

### Step 5.2: Download Local LLM Model (1GB)
```bash
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -O llm.gguf
```

---

## 6. SSL CERTIFICATE GENERATION

### Step 6.1: Generate Self-Signed SSL for Dashboard
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=US/ST=Local/L=Local/O=Nexus/CN=localhost"
```

---

## 10. ADB WIRELESS CONFIGURATION

1.  **Enable Developer Options:** Settings > About Phone > Tap Build Number 7x.
2.  **Enable Wireless Debugging:** Developer Options > Wireless Debugging.
3.  **Pair Device:** Note the IP, Port, and Pairing Code.
4.  **Connect in Termux:**
    ```bash
    adb pair [IP:PORT] [CODE]
    adb connect [IP:PORT]
    ```

---

## 13. FIRST LAUNCH & TESTING

```bash
python3 main.py
```
Navigate to `https://127.0.0.1:5000` in your browser.

---

*Build Nexus Omni. Visualize the Mind. Secure the Future. Own Your Data.*
