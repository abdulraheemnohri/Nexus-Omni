# Master Project Specification: Nexus Omni v5.0 "Horizon"
## The Ultimate Offline Sovereign Mobile Brain with Full-Stack Dashboard

**Instruction to Developer:**
This document serves as the **complete source of truth** for building **Nexus Omni v5.0**, the evolution of the offline AI agent. This version introduces a **Full-Stack Local Dashboard**, **Voice Cloning**, **Knowledge Graph Visualization**, **Multi-Profile Support**, and **Enhanced Security Protocols**. All components must operate locally on-device using Termux, Python, and Android Debug Bridge (ADB) without Root access.

---

## 1. Project Vision & Philosophy
*   **Core Goal:** A fully observable, controllable, and extensible AI entity that lives on the user's phone.
*   **The Dashboard Principle:** "If you can't see it, you can't trust it." The Dashboard provides real-time transparency into AI decisions, memory usage, and system control.
*   **Privacy First:** Zero cloud APIs. Dashboard hosted on `localhost` with self-signed SSL.
*   **Sovereignty:** User owns the data, models, UI, and control logic.
*   **Resilience:** Self-healing, energy-aware, and capable of surviving device reboots.
*   **Control:** Hybrid control model (ADB + Accessibility + Tasker Bridge + Dashboard UI).

---

## 2. Technical Stack & Requirements

### 2.1 Hardware Requirements
*   **Device:** Android 11+ (Required for Wireless ADB).
*   **RAM:** Minimum 8GB (Dashboard + LLM + Vector DB are memory-intensive).
*   **Storage:** 15GB+ free space.
*   **Battery:** 4500mAh+ recommended.

### 2.2 Software Environment
*   **OS:** Android (via **Termux** from F-Droid).
*   **Language:** Python 3.10+.
*   **Core Libraries:**
    *   `vosk` (Offline Speech-to-Text)
    *   `llama-cpp-python` (Offline LLM Inference)
    *   `sqlite-vec` (Semantic Vector Memory)
    *   `tensorflow-lite-runtime` (Offline Vision)
    *   `flask` + `flask-socketio` (Local Web Dashboard & Real-time Comms)
    *   `htmx` + `alpine.js` (Lightweight Frontend Interactivity)
    *   `cryptography` (Vault Encryption)
    *   `networkx` + `pyvis` (Knowledge Graph Visualization)
    *   `coqui-tts` (Optional: Offline Voice Cloning)
    *   `pyjwt` (Dashboard Session Management)
*   **Android Tools:**
    *   **ADB (Wireless)** for System Control.
    *   **Tasker/MacroDroid** for Biometric & Deep UI Bridge.
    *   **Termux:API** for Sensors.
    *   **Termux:Widget** for Quick Launch.

---

## 3. System Architecture

### 3.1 The Hybrid Control Layer
| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Dashboard UI** | Flask + HTMX | Visual Control, Logs, Settings, Graph Visualization |
| **WebSocket** | Flask-SocketIO | Real-time log streaming, Status updates, Live Alerts |
| **ADB Shell** | `adb shell` | System Settings, App Launch, File Mgmt |
| **Accessibility** | Tasker Bridge | UI Clicks, Screen Reading, Notifications |
| **Termux API** | `termux-*` | Sensors, SMS, Toast, Vibration |
| **Intent Broadcast** | `am broadcast` | Inter-app communication |

### 3.2 Module Interaction Diagram
```text
[User Voice/Input]      [User Dashboard Input]
      ↓                        ↓
[Voice Interface]      [Dashboard API (JWT Auth)]
      ↓                        ↓
[Agent Planner (Local LLM)] ←→ [Semantic Memory (Vector DB)]
      ↓                        ↓
[Tool Router]          [Dashboard Frontend (HTMX)]
      ├──→ [ADB Controller]         ↓
      ├──→ [Tasker Bridge]    [WebSocket Broadcast]
      ├──→ [Vision Engine]          ↓
      ├──→ [IoT Hub]          [User Browser (localhost:5000)]
      └──→ [Plugin Engine]
      ↓
[Feedback Loop (TTS/Toast/Dashboard Notification)]
```

---

## 4. Module Specifications

### 4.1 Core Brain (`main.py`)
*   **Function:** Orchestrates all modules.
*   **Feature:** **Energy Aware Mode**. Switches models based on battery.
*   **Feature:** **Self-Heal**. Watchdog timer restarts the script if frozen.
*   **Feature:** **Dashboard Heartbeat**. Sends alive signal to WebSocket every 5 seconds.

### 4.2 The Nexus Dashboard (`modules/dashboard.py`)
*   **Server:** Flask running on `127.0.0.1:5000` (Optional: `0.0.0.0` for LAN access with SSL).
*   **Security:** JWT Session Cookies, PIN Gate, Rate Limiting.
*   **Pages:**
    1.  **Home:** System Status (CPU, RAM, Battery), Active Tasks, Quick Actions.
    2.  **Console:** Live log stream (WebSocket), Manual Command Input, ADB Shell Access.
    3.  **Memory:** Searchable Vector DB, Edit/Delete Memories, Knowledge Graph View.
    4.  **Skills:** Enable/Disable Plugins, Configure IoT Topics.
    5.  **Settings:** Config.json Editor, ADB Pairing, Security Pins, SSL Management.
    6.  **Vision:** Recent Camera Captures, Object Detection Results.
    7.  **Automation:** Cron Job Manager, Workflow Builder (JSON).
    8.  **Profiles:** Switch between "Work", "Personal", "Incognito".
*   **Tech:** Server-side rendering (Jinja2) + HTMX for dynamic updates without page reloads.

### 4.3 Voice Interface (`modules/voice.py`)
*   **STT:** Vosk Model (Offline).
*   **TTS:** `termux-tts-speak` OR `coqui-tts` (for voice cloning).
*   **Wake Word:** "Hey Nexus".
*   **Privacy:** Audio processed in RAM.

### 4.4 Agentic Planner (`modules/agent.py`)
*   **Logic:** Uses Local LLM to decompose complex goals.
*   **Safety:** Requires Biometric Auth for destructive actions.
*   **Transparency:** Every step planned is pushed to Dashboard Console via WebSocket.

### 4.5 Memory System (`modules/memory.py`)
*   **Short-term:** SQLite.
*   **Long-term:** `sqlite-vec` (Semantic embeddings).
*   **Visualization:** `networkx` generates graph data for Dashboard display.
*   **Vault:** Encrypted SQLite for sensitive data.
*   **Legacy:** "Digital Will" module.

### 4.6 Control Bridge (`modules/control.py`)
*   **ADB Wireless:** Connects to `localhost:port`.
*   **Tasker Bridge:** Sends Intents for UI clicks/Biometrics.
*   **Dashboard Commands:** Allows user to click buttons in UI to trigger ADB commands safely.

### 4.7 Vision Engine (`modules/vision.py`)
*   **OCR:** `pytesseract`.
*   **Object Detection:** TensorFlow Lite (YOLO-Nano).
*   **Dashboard Integration:** Uploads captured images to local dashboard gallery for review.

### 4.8 Knowledge Graph (`modules/graph.py`)
*   **Function:** Visualizes relationships between memories.
*   **Tech:** `networkx` + `pyvis` (generates HTML graph for Dashboard).
*   **Use Case:** See how "Mom" connects to "Phone Number" and "Birthday".

---

## 5. Dashboard Implementation Details

### 5.1 Directory Structure
```text
/home/termux/nexus_omni/
├── main.py
├── config.json
├── modules/
│   ├── dashboard.py
│   ├── templates/       # HTML files
│   ├── static/          # CSS/JS
│   ├── agent.py
│   ├── memory.py
│   └── ...
├── models/
├── data/
│   ├── brain_memory.db
│   └── vault.db
└── logs/
```

### 5.2 Dashboard Code Snippet (`modules/dashboard.py`)
```python
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import functools

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECURE_RANDOM_STRING"
socketio = SocketIO(app, cors_allowed_origins="*")

# Login Decorator
def login_required(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'status': 'unauthorized'}), 401
        return f(*args, **kwargs)
    return wrap

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('dashboard.html')

@app.route('/api/command', methods=['POST'])
@login_required
def run_command():
    cmd = request.json.get('command')
    # Validate command against safety list
    # Execute via Agent
    return jsonify({'status': 'executing'})

@socketio.on('connect')
def connect():
    emit('status', {'data': 'Connected to Nexus Brain'})

@socketio.on('request_logs')
def send_logs():
    # Stream recent logs
    emit('log_stream', {'data': get_recent_logs()})

def run_dashboard():
    # Generate Self-Signed SSL for HTTPS
    # context = ('cert.pem', 'key.pem')
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)
```

### 5.3 Dashboard UI Layout (HTML/HTMX)
*   **Sidebar:** Navigation (Home, Console, Memory, Settings).
*   **Top Bar:** Battery %, CPU Load, Connection Status (Green/Red).
*   **Main Console:** Black terminal-like window streaming logs via WebSocket.
*   **Quick Actions:** Big buttons for "Lockdown", "Backup", "Sleep Mode".
*   **Memory Graph:** Interactive node-link diagram (using D3.js or Pyvis).

---

## 6. Advanced Feature Modules (v5.0 Exclusives)

### 6.1 Offline Voice Cloning
*   **Tech:** `coqui-tts` (VITS model).
*   **Function:** User records 1 minute of speech. AI fine-tunes local model to speak in user's voice.
*   **Privacy:** Model weights stored locally in `models/voice_clone.pth`.

### 6.2 Multi-Profile Support
*   **Function:** Switch between "Work" and "Personal" modes.
*   **Implementation:** Loads different `config_work.json` and `memory_work.db`.
*   **Use Case:** Keep work emails separate from personal memories.

### 6.3 Incognito Mode
*   **Function:** Toggle switch in Dashboard.
*   **Effect:** Disables memory logging, disables cloud sync (if any), disables voice recording storage.
*   **Visual:** Dashboard border turns Red when active.

### 6.4 Visual Workflow Builder
*   **Function:** Create automation rules without code.
*   **UI:** Dashboard page with Drag-and-Drop nodes (If This -> Then That).
*   **Output:** Generates JSON workflow saved to `modules/automation/`.

### 6.5 Emergency Kill Switch
*   **Function:** Physical volume button combination (e.g., Vol Up + Vol Down held for 3s).
*   **Action:** Immediately kills all AI processes, disables ADB, locks screen.
*   **Implementation:** Listens for key events via Termux API or Tasker.

### 6.6 LAN Access (Secure)
*   **Function:** Access Dashboard from PC/Tablet on same Wi-Fi.
*   **Security:** Self-signed SSL Certificate required. IP Whitelist in `config.json`.
*   **Command:** `socketio.run(app, host='0.0.0.0', port=5000, ssl_context=context)`

---

## 7. Security & Safety Protocols

### 7.1 Dashboard Security
*   **HTTPS:** Mandatory self-signed SSL. Browser warning accepted once.
*   **Authentication:** PIN + JWT Session. Session expires after 15 mins inactivity.
*   **Rate Limiting:** Max 5 login attempts per minute.
*   **CSP:** Content Security Policy headers to prevent XSS.

### 7.2 The "Asimov" Layer
*   **Hardcoded Restrictions:** No `rm -rf`, no sending money without Biometric Auth.
*   **Confirmation Loop:** Sensitive commands pause and request Dashboard confirmation.

### 7.3 Data Sovereignty
*   **Encryption:** All databases encrypted. Keys derived from User PIN.
*   **Network:** Dashboard bound to `127.0.0.1` by default. LAN access opt-in.
*   **ADB Security:** Wireless Debugging toggled off automatically after 1 hour of inactivity.

### 7.4 Intruder Detection
*   **Trigger:** 3 Failed Dashboard PIN attempts.
*   **Action:** Lock Interface, Capture Photo, Save to Vault, Log IP.

---

## 8. Installation & Setup Guide

### 8.1 Termux Preparation
```bash
# 1. Install Termux from F-Droid
# 2. Grant Storage Permission
termux-setup-storage

# 3. Update & Install Base Packages
pkg update && pkg upgrade
pkg install python python-pip clang cmake ffmpeg wget ghostscript tesseract openssl git nodejs

# 4. Install Python Libraries
pip install vosk llama-cpp-python flask flask-socketio apscheduler cryptography pandas numpy sqlite-vec paho-mqtt pillow networkx pyvis coqui-tts

# 5. Install Termux API
pkg install termux-api
```

### 8.2 SSL Certificate Generation (For Dashboard)
```bash
# Generate Self-Signed Cert for HTTPS
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
# Move to project folder
mv key.pem cert.pem ~/nexus_omni/
```

### 8.3 ADB Wireless Configuration
1.  **Enable Developer Options & Wireless Debugging.**
2.  **Pair & Connect:**
    ```bash
    adb pair 192.168.1.5:33521
    adb connect 192.168.1.5:33521
    ```
3.  **Persist:** Add to `~/.termux/boot/start_brain.sh`.

### 8.4 Dashboard Access
1.  Start Nexus Omni.
2.  Open Chrome/Firefox on phone.
3.  Navigate to `https://127.0.0.1:5000`.
4.  Accept Security Warning (Self-Signed Cert).
5.  Enter PIN (Default: `admin` -> Change immediately).

---

## 9. Configuration (`config.json`)

```json
{
  "identity": {
    "name": "Nexus",
    "version": "5.0",
    "voice_profile": "default"
  },
  "dashboard": {
    "port": 5000,
    "host": "127.0.0.1",
    "ssl_enabled": true,
    "lan_access": false,
    "session_timeout_minutes": 15
  },
  "security": {
    "pin_hash": "bcrypt_hash_here",
    "biometric_required_for": ["sms", "call", "delete", "payment"],
    "kill_switch_enabled": true
  },
  "memory": {
    "encrypt_vault": true,
    "semantic_enabled": true,
    "knowledge_graph_enabled": true
  },
  "profiles": {
    "active": "personal",
    "available": ["personal", "work", "incognito"]
  },
  "energy": {
    "llm_mode_high": 80,
    "llm_mode_medium": 40,
    "llm_mode_low": 15
  }
}
```

---

## 10. Development Roadmap

| Phase | Duration | Milestone |
| :--- | :--- | :--- |
| **1. Core** | Weeks 1-4 | Termux Setup, ADB Control, Voice I/O, SQLite Memory. |
| **2. Dashboard** | Weeks 5-8 | Flask Server, HTMX Frontend, WebSocket Logs, Auth. |
| **3. Intelligence** | Weeks 9-12 | Local LLM, Semantic Vector DB, Knowledge Graph. |
| **4. Vision & Sense** | Weeks 13-16 | TFLite Object Detection, Sensor Fusion. |
| **5. Automation** | Weeks 17-20 | Tasker Bridge, Biometric Auth, Workflow Builder. |
| **6. Advanced** | Weeks 21-24 | Voice Cloning, Multi-Profile, Incognito Mode. |
| **7. Network** | Weeks 25-28 | MQTT IoT Hub, Mesh Networking, LAN Dashboard. |
| **8. Polish** | Weeks 29-32 | Energy Management, Digital Will, Security Audit, SSL. |

---

## 11. Maintenance & Troubleshooting

| Issue | Diagnosis | Solution |
| :--- | :--- | :--- |
| **Dashboard Won't Load** | SSL Error | Ensure `cert.pem` and `key.pem` are in correct path. Accept browser warning. |
| **WebSocket Disconnects** | Port Conflict | Change port in `config.json` to 5001. |
| **ADB Disconnects** | Wireless Debugging timeout | Add watchdog script to reconnect every 5 mins. |
| **High Battery Drain** | LLM + Dashboard Running | Enable `Energy Mode` to switch to keyword-only on low battery. Close Dashboard tab. |
| **Voice Lag** | Model too large | Switch to `vosk-model-small` or reduce LLM context window. |
| **Permission Denied** | Android Security | Check Termux App Info > Permissions. Ensure Accessibility is on for Tasker. |
| **Storage Full** | Logs/Models growing | Enable `auto_backup` and `log_rotation` in config. Clear `logs/` folder. |

---

## 12. Final Developer Instructions
1.  **Modularity:** Keep every feature in a separate `modules/` file.
2.  **Dashboard First:** Design the Dashboard UI before building complex features. If you can't control it via UI, it's too hidden.
3.  **Error Handling:** Every external call (ADB, API, File) must be wrapped in `try/except` blocks.
4.  **Logging:** All actions must be logged to `nexus.log` and streamed to Dashboard Console.
5.  **Security:** Never hardcode PINs. Use `bcrypt` for hashing. Enforce HTTPS.
6.  **Ethics:** Ensure "Digital Will" and "Intruder Detection" comply with local laws.
7.  **Testing:** Test Dashboard on both Mobile Browser and Desktop Browser (if LAN enabled).

**End of Specification.**
*Build Nexus Omni. Visualize the Mind. Secure the Future. Own Your Data.*
