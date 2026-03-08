"""
LLM Interface for Nexus Omni v5.0
Supports llama-cpp models
"""

import os
from llama_cpp import Llama

class LLMInterface:
    def __init__(self, config):
        self.model_name = config.get('ai.primary_model', 'tinyllama')
        self.model_path = os.path.join('models', f"{self.model_name}.gguf")
        self.context_window = config.get('ai.context_window', 2048)
        self.threads = config.get('ai.threads', 4)
        self.llm = None

    def load(self):
        if not os.path.exists(self.model_path):
            print(f"Model not found at {self.model_path}")
            return False

        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.context_window,
                n_threads=self.threads,
                verbose=False
            )
            return True
        except Exception as e:
            print(f"Failed to load LLM: {e}")
            return False

    def generate(self, prompt, max_tokens=512, temperature=0.7):
        if not self.llm:
            return None

        output = self.llm(
            f"Q: {prompt} A: ",
            max_tokens=max_tokens,
            stop=["Q:", "\n"],
            echo=False,
            temperature=temperature
        )
        return output['choices'][0]['text'].strip()
