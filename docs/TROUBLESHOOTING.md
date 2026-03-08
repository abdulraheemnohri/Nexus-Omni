# 📟 Nexus Omni v5.0 Troubleshooting Encyclopedia

## 🔴 Common Errors

| Error | Cause | Solution |
| :--- | :--- | :--- |
| `ImportError: libandroid-spawn` | Missing build tools | Run `pkg install libandroid-spawn pkg-config` |
| `LLM Load Failed` | Model file missing | Place `tinyllama.gguf` in `models/` folder |
| `Voice Lag` | High CPU usage | Enable 'Energy Mode' in Settings |
| `ADB Disconnected` | Debugging timeout | Re-enable Wireless Debugging in Android Developer Options |

## 🛠 System Recovery
If the brain freezes:
1. Run `pkill -f app.py`
2. Clear logs: `rm logs/*.log`
3. Restart: `python app.py`

## 🛡 Security Recovery
Forgotten PIN?
- Delete `data/nexus.db` to reset (Warning: This wipes all data).
- Or restore from a previous backup in `data/backups/`.
