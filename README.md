# 📘 NEXUS OMNI v5.0 "ULTIMATE" - THE MEGA PROJECT
## The Most Advanced Offline AI Assistant for Android (Termux)

---

## 🚀 FAST INSTALL (One-Liner)
Run this command in Termux to install Nexus Omni v5.0 automatically:
```bash
pkg install -y wget && wget https://raw.githubusercontent.com/abdulraheemnohri/Nexus-Omni/main/setup.sh && chmod +x setup.sh && ./setup.sh
```

---

## 1. PROJECT OVERVIEW

### 🎯 Mission Statement
Build the world's most advanced **100% offline, privacy-first, sovereign AI assistant** that runs entirely on Android via Termux.

### ✨ v5.0 "Ultimate" Features
- **Multi-Model Intelligence:** Supports TinyLlama, Phi-2, Qwen, and Mistral models locally.
- **Semantic Memory (RAG):** Context-aware memory using `sqlite-vec` for RAG-like capabilities entirely offline.
- **Advanced Dashboard:** Multi-tab PWA for Chat, Todos, Notes, Memory, Plugins, and Automation.
- **Agentic Planning:** Uses a "Tool Router" and "Workflow Engine" for complex task decomposition.
- **Asimov Safety Layer:** Hardcoded security protocols to prevent harmful device commands.
- **Plugin Marketplace:** Extensible architecture for custom tools and IoT integrations.
- **Zero Cloud Sovereignty:** 100% data ownership. No internet connection required.

---

## 2. SYSTEM ARCHITECTURE

Nexus Omni v5.0 uses a highly modular "Layered Brain" architecture:
- **Presentation Layer:** Flask Dashboard, PWA, Terminal CLI, and Voice UI.
- **Business Logic Layer:** AI Engine (LLM), Tool Engine, Memory Manager, and Automation Scheduler.
- **Data Layer:** SQLite (Main), Vector DB (Semantic), Encrypted Vault (Secrets).
- **Infrastructure Layer:** Termux Runtime, Android API Bridge (Termux:API), and Wireless ADB.

---

## 3. INSTALLATION GUIDE

1. **Prerequisites:** Install [Termux](https://f-droid.org/en/packages/com.termux/) and [Termux:API](https://f-droid.org/en/packages/com.termux.api/) from F-Droid.
2. **Run Setup:** `./setup.sh` (This handles complex dependencies like `torch` and `libandroid-spawn`).
3. **Download LLM:** Place a `.gguf` model in the `models/` directory (Default: `tinyllama.gguf`).
4. **Launch:** `python app.py`

---

## 🛡 SECURITY & PRIVACY
- **PIN Authorization:** Mandatory access control with Bcrypt hashing.
- **AES-256 Vault:** Sensitive data is encrypted with Fernet and stored in an isolated vault.
- **Intruder Detection:** Optional photo capture on failed login attempts.
- **Digital Will:** Automated handover protocols for long-term data management.

---

## 🛠 TROUBLESHOOTING (Build Issues)
- **spawn.h missing:** Fixed by `pkg install libandroid-spawn pkg-config`.
- **Numpy/Scipy build error:** Use the `TUR` repository: `pkg install tur-repo`.
- **Whisper/Torch performance:** Ensure high-performance mode is active on your device.

---

*Your data. Your AI. Your control. Secure the Future with Nexus Omni.*
