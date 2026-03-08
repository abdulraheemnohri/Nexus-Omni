"""
Nexus Omni - Entry Point v5.0
"""
import os
import sys

# Ensure modules are in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.core.app import create_app

if __name__ == "__main__":
    app, socketio = create_app()
    # Port and host come from config handled in create_app
    socketio.run(app,
                 host=app.config.get('host', '0.0.0.0'),
                 port=app.config.get('port', 5000))
