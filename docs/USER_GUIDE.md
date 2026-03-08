# 📖 Nexus Omni v5.0 Ultimate User Guide

## 👤 User Profiles

### 1. General User (The Productivity Master)
- **Goal:** Manage daily life securely and offline.
- **Key Features:** Chat, Todos, Notes, Voice Commands.
- **How to use:**
  - Say "Hey Nexus" or click Chat.
  - Add tasks: "Remind me to buy milk".
  - Secure your data with a 4-digit PIN.

### 2. Advanced User (The Power Sovereign)
- **Goal:** Full control over automation and privacy.
- **Key Features:** Automation Engine, Mesh Networking, Semantic Memory.
- **How to use:**
  - Configure sensor triggers in the Automation tab.
  - Search your digital brain in the Memory tab.
  - Connect to other Nexus nodes via Mesh.

### 3. Developer (The Future Builder)
- **Goal:** Extend and integrate the ecosystem.
- **Key Features:** Plugin API, ADB Wireless, System Metrics.
- **How to use:**
  - Build custom plugins in `modules/plugins/`.
  - Use ADB Wireless to control the Android system directly.
  - Monitor real-time performance in the Metrics dashboard.

## 🛠 Features Deep Dive

### Semantic Memory
Nexus uses RAG (Retrieval Augmented Generation) locally. It converts your chats into vectors and stores them in `sqlite-vec`. This allows the AI to recall specific facts about you without internet.

### Asimov Safety Layer
All AI commands pass through a safety filter. Destructive system commands are blocked unless authorized via the secure bridge.

### Energy Mode
Nexus monitors your battery. If battery < 15%, it automatically switches to a quantized "Tiny" model to save power.
