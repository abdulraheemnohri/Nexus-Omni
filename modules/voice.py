"""
Voice Recognition & TTS Module
Uses: Whisper (STT), Termux TTS (Output)
"""

import subprocess
import json
try:
    import whisper
    import numpy as np
except ImportError:
    whisper = None
try:
    import pyaudio
except ImportError:
    pyaudio = None

class VoiceEngine:
    def __init__(self, config):
        self.enabled = config['voice']['enabled']
        self.sample_rate = 16000
        self.model = None
        self.audio = None
        self.stream = None
        if self.enabled and whisper:
            print("[*] Loading Whisper model for voice STT...")
            self.model = whisper.load_model("tiny")

    def start_listening(self):
        """Start audio stream"""
        if not self.enabled or not pyaudio: return
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=8000
        )
        self.stream.start_stream()

    def listen(self, timeout=5):
        """Listen for speech and return text using Whisper"""
        if not self.enabled or not self.model or not self.stream:
            return None

        try:
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                return None

            audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            if np.abs(audio_np).max() > 0.05:
                result = self.model.transcribe(audio_np, fp16=False)
                return result.get('text', '').strip()

            return None
        except Exception as e:
            print(f"Voice listen error: {e}")
            return None

    def speak(self, text):
        """Text-to-Speech using Termux"""
        if not self.enabled:
            print(f"NEXUS (Muted): {text}")
            return

        print(f"NEXUS: {text}")
        try:
            subprocess.run(
                ['termux-tts-speak', text],
                check=False,
                timeout=10
            )
        except Exception as e:
            print(f"TTS error: {e}")

    def stop(self):
        """Stop audio stream"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
