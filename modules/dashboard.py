from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_socketio import SocketIO, emit
import jwt
import datetime
import functools
import bcrypt
import os
import logging
from modules.utils import get_logger, load_config

logger = get_logger("Dashboard")

app = Flask(__name__, template_folder='templates', static_folder='static')
config = load_config()
app.config['SECRET_KEY'] = config['dashboard'].get('secret_key', os.urandom(24))
socketio = SocketIO(app, cors_allowed_origins="*")

class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        socketio.emit('log_stream', {'data': log_entry})

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    pin = request.form.get('pin')
    stored_hash = config['security']['pin_hash']

    if bcrypt.checkpw(pin.encode(), stored_hash.encode()):
        session['logged_in'] = True
        token = jwt.encode({
            'user': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config['dashboard']['session_timeout_minutes'])
        }, app.config['SECRET_KEY'], algorithm="HS256")
        session['token'] = token
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/graph')
@token_required
def show_graph():
    return render_template('graph_view.html')

@app.route('/api/config', methods=['GET', 'POST'])
@token_required
def manage_config():
    global config
    if request.method == 'POST':
        new_config = request.json
        with open('config.json', 'w') as f:
            import json
            json.dump(new_config, f, indent=2)
        config = new_config
        return jsonify({'status': 'updated'})
    return jsonify(config)

@app.route('/api/adb', methods=['POST'])
@token_required
def run_adb():
    command = request.json.get('command', '').split()
    logger.info(f"Dashboard triggered ADB: {command}")
    return jsonify({'status': 'sent', 'command': command})

@app.route('/api/memory/search')
@token_required
def search_memory():
    query = request.args.get('q', '')
    logger.info(f"Memory search: {query}")
    return jsonify({'results': []})

@app.route('/api/profile/switch', methods=['POST'])
@token_required
def switch_profile():
    profile = request.json.get('profile')
    logger.info(f"Dashboard requested profile switch: {profile}")
    return jsonify({'status': 'requested', 'profile': profile})

@app.route('/api/incognito', methods=['POST'])
@token_required
def toggle_incognito():
    state = request.json.get('state')
    logger.info(f"Dashboard toggled incognito: {state}")
    return jsonify({'status': 'updated', 'state': state})

@app.route('/api/kill', methods=['POST'])
@token_required
def trigger_kill():
    logger.critical("KILL SWITCH TRIGGERED FROM DASHBOARD")
    return jsonify({'status': 'terminating'})

@app.route('/api/plugins', methods=['GET'])
@token_required
def list_plugins():
    plugins_dir = os.path.join(os.path.dirname(__file__), '..', 'plugins')
    files = [f for f in os.listdir(plugins_dir) if f.endswith('.py') and f != '__init__.py']
    return jsonify({'plugins': files})

@socketio.on('connect')
def connect():
    logger.info("Client connected to WebSocket.")
    emit('status', {'data': 'Connected to Nexus Brain'})

def stream_logs(log_line):
    socketio.emit('log_stream', {'data': log_line})

def broadcast_telemetry(stats):
    socketio.emit('telemetry', stats)

def run_dashboard(config_arg):
    # This matches the signature expected by main.py
    port = config_arg['dashboard']['port']
    host = config_arg['dashboard']['host']
    ssl_enabled = config_arg['dashboard']['ssl_enabled']

    if ssl_enabled:
        context = ('cert.pem', 'key.pem')
        socketio.run(app, host=host, port=port, ssl_context=context, debug=False, allow_unsafe_werkzeug=True)
    else:
        socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True)
