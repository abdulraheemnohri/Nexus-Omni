#!/usr/bin/env python3
"""
Agent Planner - Local LLM
"""

import os
from llama_cpp import Llama
import logging

class AgentPlanner:
    def __init__(self, config, controller, memory):
        self.config = config
        self.controller = controller
        self.memory = memory
        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'llm.gguf')
        self.logger = logging.getLogger('Agent')
        self._init_llm()

    def _init_llm(self):
        if not os.path.exists(self.model_path):
            self.logger.warning(f"LLM model not found at {self.model_path}. Agent limited.")
            self.llm = None
            return

        self.llm = Llama(model_path=self.model_path, n_ctx=2048)
        self.logger.info("Local LLM initialized.")

    def process(self, text):
        self.logger.info(f"Processing command: {text}")
        if self.asimov_check(text):
            return "Safety violation blocked."

        if not self.llm:
            return "LLM unavailable. Manual mode only."

        # Structured prompt for planning
        prompt = f"### System: You are Nexus Omni, a sovereign mobile AI. User: {text}\n### Response:"

        try:
            response = self.llm(prompt, max_tokens=128, stop=["User:"])
            output = response['choices'][0]['text'].strip()
            self.logger.info(f"Nexus Plan: {output}")
            return output
        except Exception as e:
            self.logger.error(f"LLM inference error: {e}")
            return "Failed to generate plan."

    def asimov_check(self, command):
        forbidden = ["rm -rf", "mkfs"]
        for f in forbidden:
            if f in command:
                self.logger.warning(f"Blocked dangerous command: {command}")
                return True
        return False
