"""
Local LLM Integration Module
Supports: TinyLlama, Phi-2, Qwen, Gemma
"""

from llama_cpp import Llama
import os

class LocalLLM:
    def __init__(self, config):
        self.model_path = config['ai']['model_path']
        self.context_size = config['ai']['context_size']
        self.threads = config['ai']['threads']
        self.llm = None
        self.loaded = False

    def load(self):
        """Load model into memory"""
        if not os.path.exists(self.model_path):
            print(f"⚠️ Model not found: {self.model_path}")
            return False

        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.context_size,
                n_threads=self.threads,
                n_gpu_layers=0,  # CPU only for mobile
                n_batch=512,
                use_mlock=True,
                verbose=False
            )
            self.loaded = True
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False

    def generate(self, prompt, max_tokens=256):
        """Generate text response"""
        if not self.loaded:
            return None

        try:
            # Format prompt for TinyLlama chat
            formatted_prompt = f"<|system|>\nYou are Nexus Omni, a helpful offline AI assistant.<|user|>\n{prompt}<|assistant|>\n"

            output = self.llm(
                formatted_prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stop=['<|user|>', '<|system|>', 'User:'],
                echo=False
            )

            return output['choices'][0]['text'].strip()
        except Exception as e:
            print(f"❌ Generation error: {e}")
            return None

    def unload(self):
        """Free memory"""
        if self.llm:
            del self.llm
            self.loaded = False
