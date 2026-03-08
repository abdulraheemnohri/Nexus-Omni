"""
Nexus Omni - Main Backend
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
import threading
import time
import eventlet

from modules.ai_engine import AIEngine
from modules.monitor import Monitor
from modules.security import Security

# Initialize App
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Load Config
config_path = 'config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

# Initialize Engines
ai = AIEngine(config)
monitor = Monitor()
security = Security(config)

# API Routes
@app.route('/')
def index():
    return render_template('dashboard.html', config=config)

@app.route('/api/status')
def get_status():
    return jsonify(monitor.get_stats())

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message'}), 400

    result = ai.process(message)
    return jsonify(result)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify({'todos': ai.db.get_todos()})

# WebSocket Logic
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'status': 'online', 'version': config['app']['version']})

@socketio.on('chat_message')
def handle_chat(data):
    message = data.get('message', '')
    result = ai.process(message)
    emit('ai_response', result)

# Background Telemetry Thread
def telemetry_loop():
    while True:
        stats = monitor.get_stats()
        socketio.emit('telemetry', stats)
        time.sleep(5)

if __name__ == '__main__':
    # Start telemetry thread
    threading.Thread(target=telemetry_loop, daemon=True).start()

    port = config['app']['port']
    host = config['app']['host']

    print(f"🚀 Nexus Omni v{config['app']['version']} running at http://{host}:{port}")
    socketio.run(app, host=host, port=port, debug=config['app']['debug'])
