import paho.mqtt.client as mqtt
import socket
import threading
import json
from modules.utils import get_logger

logger = get_logger("Network")

class NetworkManager:
    def __init__(self, config):
        self.config = config
        self.mqtt_enabled = config['network']['mqtt_enabled']
        self.mesh_enabled = config['network']['mesh_enabled']
        self._init_mqtt()
        self._init_mesh()

    def _init_mqtt(self):
        if not self.mqtt_enabled:
            return
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        try:
            # Connecting to local broker
            self.client.connect("127.0.0.1", 1883, 60)
            threading.Thread(target=self.client.loop_forever, daemon=True).start()
            logger.info("MQTT Client started.")
        except Exception as e:
            logger.error(f"MQTT connection failed: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected to MQTT broker with result code {rc}")
        client.subscribe("nexus/commands")

    def _on_message(self, client, userdata, msg):
        logger.info(f"Received MQTT message: {msg.topic} {msg.payload}")

    def _init_mesh(self):
        if not self.mesh_enabled:
            return
        self.mesh_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mesh_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        threading.Thread(target=self._mesh_listener, daemon=True).start()
        logger.info("Mesh Listener started.")

    def _mesh_listener(self):
        self.mesh_socket.bind(('', 5555))
        while True:
            data, addr = self.mesh_socket.recvfrom(1024)
            logger.info(f"Received mesh broadcast from {addr}: {data}")

    def broadcast_mesh(self, message):
        logger.info(f"Broadcasting to mesh: {message}")
        self.mesh_socket.sendto(message.encode(), ('<broadcast>', 5555))

    def publish_mqtt(self, topic, payload):
        if self.mqtt_enabled:
            self.client.publish(topic, payload)
