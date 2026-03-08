"""
MQTT IoT Hub for v5.0
Integration with smart home devices
"""
try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

class MQTTBroker:
    def __init__(self, host='localhost', port=1883):
        self.host = host
        self.port = port
        self.client = None
        if mqtt:
            self.client = mqtt.Client()

    def connect(self):
        if self.client:
            try:
                self.client.connect(self.host, self.port)
                self.client.loop_start()
                return True
            except: pass
        return False

    def publish(self, topic, message):
        if self.client:
            self.client.publish(topic, message)
