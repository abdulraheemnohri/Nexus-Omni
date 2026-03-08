#!/usr/bin/env python3
"""
Voice Interface Module - Offline STT/TTS
"""

import os
import json
import subprocess
from vosk import Model, KaldiRecognizer
try:
    import pyaudio
except ImportError:
    pyaudio = None

class VoiceInterface:
    def __init__(self, config):
        self.config = config
        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'vosk-model')
        self.sample_rate = 16000
        self.wake_word = config['voice']['wake_word'].lower()

        # Initialize Vosk model
        if not os.path.exists(self.model_path):
            print(f"Warning: Vosk model not found at {self.model_path}. Voice input disabled.")
            self.model = None
            return

        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

        # Initialize audio
        if pyaudio:
            self.p = pyaudio.PyAudio()
            self.stream = None
        else:
            self.p = None
            self.stream = None

    def speak(self, text):
        """Text-to-Speech using Termux"""
        print(f"NEXUS: {text}")
        try:
            # Using termux-tts-speak
            subprocess.run(["termux-tts-speak", text], check=False, timeout=10)
        except Exception as e:
            print(f"TTS Error: {e}")

    def listen(self, timeout=5):
        """Listen for voice command and return recognized text"""
        if not self.p or not self.model:
            return None

        try:
            if self.stream is None:
                self.stream = self.p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=8000
                )
                self.stream.start_stream()

            # Read audio data
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                return None

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    return text
            else:
                # Partial result
                pass

            return None

        except Exception as e:
            print(f"Voice listen error: {e}")
            return None

    def close(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()
