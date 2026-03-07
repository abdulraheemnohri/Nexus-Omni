import os
import subprocess
from vosk import Model, KaldiRecognizer
try:
    import pyaudio
except ImportError:
    pyaudio = None
from modules.utils import get_logger

logger = get_logger("Voice")

class VoiceInterface:
    def __init__(self, config):
        self.config = config
        self.model_path = "models/vosk-model-small-en-us-0.15"
        self._init_stt()

    def _init_stt(self):
        if not os.path.exists(self.model_path):
            logger.warning(f"Vosk model not found at {self.model_path}. STT disabled.")
            self.model = None
            return

        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        logger.info("Vosk STT initialized.")

    def speak(self, text):
        logger.info(f"Speaking: {text}")
        try:
            # Using termux-tts-speak
            subprocess.run(["termux-tts-speak", text])
        except Exception as e:
            logger.error(f"TTS failed: {e}")

    def listen(self):
        if not self.model:
            return None

        # This is a blocking call for a real environment
        # In this sandbox, we'll return a stub or implement a timeout
        logger.info("Listening for voice input...")
        # Mocking audio stream for now
        return None

    def clone_voice(self, audio_path):
        # Placeholder for coqui-tts voice cloning
        logger.info(f"Cloning voice from {audio_path}...")
        return True
