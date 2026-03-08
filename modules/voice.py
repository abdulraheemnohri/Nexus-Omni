#!/usr/bin/env python3
"""
Voice Interface Module - Offline STT/TTS
"""

import os
import json
import subprocess
import whisper
import numpy as np
try:
    import pyaudio
except ImportError:
    pyaudio = None

class VoiceInterface:
    def __init__(self, config):
        self.config = config
        self.model_name = config['voice'].get('whisper_model', 'tiny')
        self.sample_rate = 16000
        self.wake_word = config['voice']['wake_word'].lower()

        # Initialize Whisper model
        try:
            print(f"[*] Loading Whisper model: {self.model_name}...")
            self.model = whisper.load_model(self.model_name)
            print("✓ Whisper STT initialized.")
        except Exception as e:
            print(f"Warning: Failed to load Whisper model: {e}. Voice input disabled.")
            self.model = None

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
        """Listen for voice command and return recognized text using Whisper"""
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

            # Convert to float32 numpy array for Whisper
            audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

            # Simple threshold for speech detection (stub)
            if np.abs(audio_np).max() > 0.05:
                result = self.model.transcribe(audio_np, fp16=False)
                text = result.get("text", "").strip()
                if text:
                    return text

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
