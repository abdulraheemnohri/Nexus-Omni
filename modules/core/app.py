"""
Nexus Omni Main Application v5.0
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import functools

from modules.core.config import ConfigManager
from modules.database.sqlite_handler import DatabaseManager
from modules.monitoring.health import HealthMonitor
from modules.plugins.loader import PluginLoader
from modules.ai.engine import AIEngine

def create_app():
    app = Flask(__name__,
                static_folder='../../static',
                template_folder='../../templates')

    # Configuration
    config_path = os.path.join(os.getcwd(), 'config.json')
    cfg = ConfigManager(config_path)
    app.config.update(cfg.config['app'])
    app.config['SECRET_KEY'] = cfg.get('app.secret_key') or "dev_secret"

    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

    # Initialize Core Components
    db = DatabaseManager(cfg.get('database.path'))
    monitor = HealthMonitor()
    plugins = PluginLoader(os.path.join(os.getcwd(), 'modules', 'plugins'))
    plugins.load_plugins()
    ai = AIEngine(cfg, db)

    # Auth Decorator
    def login_required(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if cfg.get('security.pin_enabled') and 'user_id' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    # Routes
    @app.route('/')
    @login_required
    def index():
        return render_template('dashboard.html', config=cfg.config)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if not cfg.get('security.pin_enabled'):
            session['user_id'] = 1 # Default admin
            return redirect(url_for('index'))

        if request.method == 'POST':
            pin = request.form.get('pin')
            # For v5.0, we support multiple users, but default to 'admin'
            user = db.get_user('admin')
            if not user:
                # Setup first user if none exists
                from modules.security.auth import hash_pin
                db.add_user('admin', hash_pin(pin))
                user = db.get_user('admin')

            from modules.security.auth import verify_pin
            if verify_pin(pin, user['pin_hash']):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('index'))
            return render_template('login.html', error="Invalid PIN", config=cfg.config)

        return render_template('login.html', config=cfg.config)

    @app.route('/api/status')
    @login_required
    def get_status():
        return jsonify(monitor.get_stats())

    @app.route('/api/plugins')
    @login_required
    def list_plugins():
        return jsonify(plugins.list_plugins())

    @app.route('/api/todos', methods=['GET', 'POST'])
    @login_required
    def manage_todos():
        user_id = session.get('user_id')
        if request.method == 'POST':
            data = request.json
            db.add_todo(user_id, data.get('task'), data.get('priority', 'medium'))
            return jsonify({'status': 'added'})
        return jsonify({'todos': db.get_todos(user_id)})

    # SocketIO
    @socketio.on('connect')
    def handle_connect():
        if cfg.get('security.pin_enabled') and 'user_id' not in session:
            return False
        emit('connected', {'status': 'online', 'version': app.config['version']})

    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, host=app.config['host'], port=app.config['port'])
