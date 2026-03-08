#!/usr/bin/env python3
"""
Nexus Omni v5.0 - Main Entry Point
Offline Sovereign Mobile Brain
"""

import os
import sys
import json
import time
import signal
import logging
import threading
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

# Import core modules
from dashboard import run_dashboard, SocketIOHandler, broadcast_telemetry
from voice import VoiceInterface
from memory import BrainMemory
from control import ADBController
from agent import AgentPlanner
from sensors import SensorFusion
from vault import SecureVault
from autopilot import AutoPilot
from modules.vision import VisionEngine
from modules.graph import GraphManager
from utils import load_config, generate_ssl_cert

class NexusOmni:
    def __init__(self, profile=None):
        self.config = self._load_profile(profile)
        self.setup_logging()
        self.running = False

        # Initialize SSL if needed
        if self.config['dashboard']['ssl_enabled']:
            generate_ssl_cert()

        print("=" * 50)
        print("NEXUS OMNI v5.0 'HORIZON'")
        print("=" * 50)
        print(f"Initializing {self.config['identity']['name']}...")

        # State
        self.incognito_mode = False

        # Initialize core components
        self.memory = BrainMemory(self.config)
        self.vault = SecureVault(self.config)
        self.controller = ADBController(self.config['network']['adb_ip'])
        self.sensors = SensorFusion()
        self.voice = VoiceInterface(self.config)
        self.agent = AgentPlanner(self.config, self.controller, self.memory)
        self.autopilot = AutoPilot(self.config, self.controller)
        self.plugins = self._load_plugins()

        print("✓ All modules initialized")
        print("=" * 50)

    def _load_profile(self, profile):
        base_config = load_config()
        if not profile:
            profile = base_config['profiles']['active']

        profile_file = f"config_{profile}.json"
        if os.path.exists(profile_file):
            with open(profile_file, 'r') as f:
                return json.load(f)
        return base_config

    def setup_logging(self):
        log_file = self.config['logging']['file']
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        handlers = [
            logging.FileHandler(log_file),
            logging.StreamHandler(),
            SocketIOHandler()
        ]

        logging.basicConfig(
            level=getattr(logging, self.config['logging']['level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
        self.logger = logging.getLogger('NexusOmni')

    def _load_plugins(self):
        plugins = []
        if not os.path.exists("plugins"):
            os.makedirs("plugins")

        for file in os.listdir("plugins"):
            if file.endswith(".py") and file != "__init__.py":
                self.logger.info(f"Found plugin: {file}")
                plugins.append(file)
        return plugins

    def signal_handler(self, sig, frame):
        print("\n⚠ Shutdown signal received")
        self.running = False
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        print("Cleaning up resources...")
        self.memory.close()
        self.vault.close()
        print("✓ Cleanup complete")

    def health_check(self):
        battery = self.sensors.get_battery()
        if battery.get('percentage', 100) < self.config['energy']['llm_mode_low']:
            self.logger.warning("Low battery - switching to power save mode")
        return True

    def telemetry_loop(self):
        while self.running:
            try:
                stats = self.sensors.get_system_stats()
                battery = self.sensors.get_battery()
                stats['battery'] = battery.get('percentage', 100)
                stats['battery_status'] = battery.get('status', 'unknown')
                broadcast_telemetry(stats)
            except:
                pass
            time.sleep(5)

    def energy_management_loop(self):
        while self.running:
            battery = self.sensors.get_battery()
            percent = battery.get('percentage', 100)
            if percent < self.config['energy']['llm_mode_low']:
                # Keyword only
                pass
            elif percent < self.config['energy']['llm_mode_medium']:
                # Quantized
                pass
            time.sleep(60)

    def process_command(self, text):
        if self.incognito_mode:
            self.logger.info("Processing in Incognito Mode (No persistence)")
            return self.agent.process(text)

        # Save to memory first
        self.memory.save(text, category="user_input")
        response = self.agent.process(text)
        self.memory.save(response, category="ai_response")
        return response

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # Start background threads
        threading.Thread(target=self.energy_management_loop, daemon=True).start()
        threading.Thread(target=self.telemetry_loop, daemon=True).start()

        # Start dashboard
        dashboard_thread = threading.Thread(target=run_dashboard, args=(self.config,), daemon=True)
        dashboard_thread.start()
        print(f"✓ Dashboard started at https://{self.config['dashboard']['host']}:{self.config['dashboard']['port']}")

        # Start autopilot
        self.autopilot.start()
        print("✓ AutoPilot scheduler started")

        self.running = True
        self.logger.info("Nexus Omni is now ONLINE")
        self.voice.speak(f"{self.config['identity']['name']} Omni online. How can I help?")

        while self.running:
            try:
                self.health_check()
                command = self.voice.listen()
                if command:
                    self.logger.info(f"Voice command: {command}")
                    self.agent.process(command)
                time.sleep(0.5)
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"Main loop error: {e}")
                time.sleep(5)

        self.cleanup()

if __name__ == "__main__":
    try:
        nexus = NexusOmni()
        nexus.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
