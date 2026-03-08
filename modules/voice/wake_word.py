"""
Wake Word Detection (Keyword Spotting) for v5.0
Stub for offline wake-word recognition
"""
import time

class WakeWordEngine:
    def __init__(self, keyword="Hey Nexus"):
        self.keyword = keyword
        self.active = False

    def start_listening(self):
        """Mock listener - would use PyAudio and a small keyword model in production"""
        self.active = True
        print(f"👂 Listening for wake word: '{self.keyword}'")

    def stop_listening(self):
        self.active = False

    def detect(self):
        # Placeholder for real detection logic
        return False
