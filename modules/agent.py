import os
from llama_cpp import Llama
from modules.utils import get_logger

logger = get_logger("Agent")

class AgentPlanner:
    def __init__(self, config):
        self.config = config
        self.model_path = "models/llm.gguf"
        self._init_llm()

    def _init_llm(self):
        if not os.path.exists(self.model_path):
            logger.warning(f"LLM model not found at {self.model_path}. Agent limited.")
            self.llm = None
            return

        self.llm = Llama(model_path=self.model_path, n_ctx=2048)
        logger.info("Local LLM initialized.")

    def plan(self, user_input):
        logger.info(f"Planning for: {user_input}")

        if self.asimov_check(user_input):
            return "Action blocked by Asimov safety layer."

        if not self.llm:
            return "LLM unavailable. Manual mode only."

        # Simplified prompt for planning
        prompt = f"User: {user_input}\nNexus:"
        response = self.llm(prompt, max_tokens=256)
        output = response['choices'][0]['text'].strip()
        logger.info(f"Agent Plan: {output}")
        return output

    def asimov_check(self, command):
        # Physical/System protection layer
        forbidden = ["rm -rf /", "mkfs", "dd if="]
        for f in forbidden:
            if f in command:
                logger.warning(f"Dangerous command detected: {command}")
                return True
        return False

    def decompose_goal(self, goal):
        # Logic to break down "Document this receipt" into steps
        # This would typically be a specific LLM prompt
        return ["Capture Screen", "OCR", "Store in Memory"]
