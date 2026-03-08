# Nexus Omni v5.0 "Horizon" Instructions

This project has been upgraded to v5.0 "Horizon". Follow the specifications in V5_SPEC.md for all implementation details.
The user has explicitly commanded: "procssed with v5".

Key changes from v4.0:
- Directory structure: `data/`, `logs/`, `modules/templates/`, `modules/static/`.
- Technology stack: `flask-socketio`, `networkx`, `pyvis`, `pyjwt`, `bcrypt`, `htmx`, `alpine.js`.
- Features: Full-stack dashboard, Knowledge Graph, Multi-profile support, SSL/JWT security.
- Memory: SQLite in `data/`, `sqlite-vec` integration.
- Logging: `logs/nexus.log`.
