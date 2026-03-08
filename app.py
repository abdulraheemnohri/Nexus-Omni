"""
Nexus Omni - Main Backend v4.0
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
import threading
import time
import eventlet
import functools

from modules.ai_engine import AIEngine
from modules.monitor import Monitor
from modules.security import Security
from modules.voice import VoiceEngine
from modules.tools import generate_password

# Initialize App
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Load Config
config_path = 'config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

app.config['SECRET_KEY'] = config.get('app', {}).get('secret_key', os.urandom(24))

# Initialize Engines
ai = AIEngine(config)
monitor = Monitor()
security = Security(config)
voice = VoiceEngine(config)

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not config['security']['pin_enabled']:
            return f(*args, **kwargs)
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
@login_required
def index():
    return render_template('dashboard.html', config=config)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not config['security']['pin_enabled']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        pin = request.form.get('pin')
        stored_hash = ai.db.get_setting('pin_hash')

        # Initial PIN setup if none exists
        if not stored_hash:
            new_hash = security.hash_pin(pin)
            ai.db.save_setting('pin_hash', new_hash)
            session['logged_in'] = True
            return redirect(url_for('index'))

        if security.verify_pin(pin, stored_hash):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            security.log_failed_attempt(ai.db, request.remote_addr)
            return render_template('login.html', error="Invalid PIN", config=config)

    return render_template('login.html', config=config)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API Endpoints
@app.route('/api/status')
@login_required
def get_status():
    return jsonify(monitor.get_stats())

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    message = data.get('message', '')
    if not message: return jsonify({'error': 'No message'}), 400
    return jsonify(ai.process(message))

@app.route('/api/todos', methods=['GET', 'POST'])
@login_required
def manage_todos():
    if request.method == 'POST':
        data = request.json
        ai.db.add_todo(data.get('task'), data.get('priority', 'medium'))
        return jsonify({'status': 'added'})
    return jsonify({'todos': ai.db.get_todos()})

@app.route('/api/notes', methods=['GET', 'POST'])
@login_required
def manage_notes():
    if request.method == 'POST':
        data = request.json
        ai.db.add_note(data.get('title'), data.get('content'), data.get('tags', ''))
        return jsonify({'status': 'added'})
    return jsonify({'notes': ai.db.get_notes()})

@app.route('/api/tools/password')
@login_required
def api_password():
    length = int(request.args.get('length', 16))
    return jsonify({'password': generate_password(length)})

@app.route('/api/system/export')
@login_required
def export_data():
    return jsonify(ai.db.export_all_data())

# API Endpoints
@app.route('/api/voice/speak', methods=['POST'])
@login_required
def voice_speak():
    data = request.json
    text = data.get('text', '')
    voice.speak(text)
    return jsonify({'status': 'speaking'})

# WebSocket Logic
@socketio.on('connect')
def handle_connect():
    if config['security']['pin_enabled'] and 'logged_in' not in session:
        return False # Disconnect unauthorized
    emit('connected', {'status': 'online', 'version': config['app']['version']})

@socketio.on('chat_message')
def handle_chat(data):
    if config['security']['pin_enabled'] and 'logged_in' not in session:
        return
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
    threading.Thread(target=telemetry_loop, daemon=True).start()
    port = config['app']['port']
    host = config['app']['host']
    socketio.run(app, host=host, port=port, debug=config['app']['debug'])
