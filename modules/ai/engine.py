"""
AI Engine v5.0 with Multi-Model Support and Asimov Safety Layer
"""

import datetime

class AIEngine:
    def __init__(self, config, db):
        self.config = config
        self.db = db
        from modules.ai.llm import LLMInterface
        self.llm = LLMInterface(config)
        self.llm_available = self.llm.load()
        from modules.vision.engine import VisionEngine
        self.vision = VisionEngine(config)

        # Asimov Safety Layer - Hardcoded restrictions
        self.restricted_keywords = [
            'rm -rf', 'format c:', 'delete system', 'drop table',
            'send money', 'transfer funds', 'sudo'
        ]

    def process(self, user_id, text):
        """Main processing loop with safety check"""
        text_lower = text.lower().strip()

        # 1. Safety Check (Asimov Layer)
        if self.is_dangerous(text_lower):
            response = "⚠️ This action is sensitive or potentially harmful. Please verify via Biometric/PIN or rephrase."
            self.db.save_chat(user_id, 'ai', response)
            return {'response': response, 'source': 'safety_layer'}

        # 2. Rule-based check (Fast path)
        response = self.rule_based_check(user_id, text_lower)
        if response:
            self.db.save_chat(user_id, 'ai', response)
            return {'response': response, 'source': 'rules'}

        # 3. LLM Processing
        if self.llm_available:
            try:
                llm_response = self.llm.generate(text)
                if llm_response:
                    self.db.save_chat(user_id, 'ai', llm_response)
                    return {'response': llm_response, 'source': 'llm'}
            except Exception as e:
                print(f"LLM Error: {e}")

        # 4. Fallback
        response = "I'm not sure how to help with that yet. Should I search my memory?"
        self.db.save_chat(user_id, 'ai', response)
        return {'response': response, 'source': 'fallback'}

    def is_dangerous(self, text):
        return any(k in text for k in self.restricted_keywords)

    def rule_based_check(self, user_id, text):
        if 'time' in text:
            return f"It is currently {datetime.datetime.now().strftime('%H:%M')}."
        if 'date' in text:
            return f"Today is {datetime.datetime.now().strftime('%Y-%m-%d')}."
        if 'add task' in text:
            task = text.replace('add task', '').strip()
            self.db.add_todo(user_id, task)
            return f"Added task: {task}"

        if 'read this' in text or 'extract text' in text:
            # Placeholder for image handling logic
            return "Vision Engine: Ready to extract text. (Please provide image path via tool/API)"

        return None
