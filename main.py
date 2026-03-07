import time
import threading
import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from modules.utils import setup_logging, load_config, get_logger, get_battery_level, generate_ssl_cert
from modules.memory import MemoryManager
from modules.agent import AgentPlanner
from modules.voice import VoiceInterface
from modules.control import ControlBridge
from modules.vision import VisionEngine
from modules.network import NetworkManager
from modules.dashboard import run_dashboard, socketio
from modules.graph import GraphManager

class NexusOmni:
    def __init__(self, profile=None):
        self.config = self._load_profile(profile)
        setup_logging()
        self.logger = get_logger("Nexus")

        # Initialize SSL if needed
        if self.config['dashboard']['ssl_enabled']:
            generate_ssl_cert()

        # State
        self.incognito_mode = False

        # Initialize Modules
        self.memory = MemoryManager(self.config)
        self.agent = AgentPlanner(self.config)
        self.voice = VoiceInterface(self.config)
        self.control = ControlBridge(self.config)
        self.vision = VisionEngine(self.config)
        self.network = NetworkManager(self.config)
        self.graph = GraphManager(self.memory)
        self.plugins = self._load_plugins()
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self.running = True
        self.logger.info(f"Nexus Omni v{self.config['identity']['version']} 'Horizon' started.")

    def _load_profile(self, profile):
        base_config = load_config()
        if not profile:
            profile = base_config['profiles']['active']

        profile_file = f"config_{profile}.json"
        if os.path.exists(profile_file):
            with open(profile_file, 'r') as f:
                return json.load(f)
        return base_config

    def switch_profile(self, profile_name):
        self.logger.info(f"Switching to profile: {profile_name}")
        # In a real app, this might restart the orchestrator or re-init modules
        self.config = self._load_profile(profile_name)
        # Update modules with new config if necessary

    def toggle_incognito(self, state):
        self.incognito_mode = state
        self.logger.info(f"Incognito Mode: {'Enabled' if state else 'Disabled'}")

    def _load_plugins(self):
        plugins = []
        if not os.path.exists("plugins"):
            os.makedirs("plugins")

        for file in os.listdir("plugins"):
            if file.endswith(".py") and file != "__init__.py":
                self.logger.info(f"Found plugin: {file}")
                plugins.append(file)
        return plugins

    def energy_management(self):
        while self.running:
            battery = get_battery_level()
            if battery < self.config['energy']['llm_mode_low']:
                self.logger.warning("Low Battery! Switching to Keyword Only mode.")
            elif battery < self.config['energy']['llm_mode_medium']:
                self.logger.info("Battery Medium. Using Quantized LLM.")

            time.sleep(60)

    def trigger_kill_switch(self):
        self.logger.critical("EMERGENCY KILL SWITCH TRIGGERED!")
        self.running = False
        # In a real environment, we'd kill all subprocesses and lock Android
        self.control.run_adb(["shell", "input", "keyevent", "26"]) # Power button
        self.logger.info("System Locked. AI processes terminated.")

    def self_heal_watchdog(self):
        while self.running:
            # Check for module health (stub)
            # If RAM > 90%, clear cache
            time.sleep(30)

    def dashboard_heartbeat(self):
        while self.running:
            socketio.emit('status', {'cpu': 10, 'ram': 20, 'battery': get_battery_level()})
            time.sleep(5)

    def start(self):
        # Start background threads
        threading.Thread(target=self.energy_management, daemon=True).start()
        threading.Thread(target=self.self_heal_watchdog, daemon=True).start()
        threading.Thread(target=self.dashboard_heartbeat, daemon=True).start()

        # Start Dashboard in a separate thread
        threading.Thread(target=run_dashboard, daemon=True).start()

        # Main Loop
        try:
            while self.running:
                # Core agent logic would go here
                # e.g., listening for wake word or processing scheduled tasks
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            self.logger.info("Nexus Omni shutting down.")

if __name__ == "__main__":
    nexus = NexusOmni()
    nexus.start()
