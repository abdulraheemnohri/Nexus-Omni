"""
AI Logic & Decision Making
"""

import datetime
from modules.ai_model import LocalLLM
from modules.database import Database

class AIEngine:
    def __init__(self, config):
        self.config = config
        self.db = Database(config['database']['path'])
        self.llm = LocalLLM(config)
        self.llm_available = self.llm.load()
        self.name = config['app']['name']
        self.user_name = self.db.get_setting('user_name', 'User')

    def process(self, text):
        """Main processing - uses LLM if available, else rules"""
        text_lower = text.lower().strip()
        self.db.save_chat('user', text)

        # 1. Check for specific tool commands first
        response = self.rule_based_check(text_lower)
        if response:
            self.db.save_chat('ai', response)
            return {'response': response, 'source': 'rules'}

        # 2. Use LLM if available
        if self.llm_available:
            try:
                llm_response = self.llm.generate(text)
                if llm_response:
                    self.db.save_chat('ai', llm_response)
                    return {'response': llm_response, 'source': 'llm'}
            except Exception as e:
                print(f"LLM failed: {e}")

        # 3. Final Fallback
        response = f"I heard you say: '{text}'. How can I help with that?"
        self.db.save_chat('ai', response)
        return {'response': response, 'source': 'fallback'}

    def rule_based_check(self, text):
        """Simple rule-based responses for common tools"""
        if any(greet in text for greet in ['hello', 'hi', 'hey']):
            return f"Hello {self.user_name}! I am {self.name}, your offline assistant."

        elif 'time' in text:
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."

        elif 'date' in text:
            return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."

        elif 'my name is' in text:
            name = text.split('my name is')[-1].strip().title()
            self.db.save_setting('user_name', name)
            self.user_name = name
            return f"Nice to meet you, {name}! I've updated my records."

        elif 'add task' in text or 'add todo' in text:
            task = text.replace('add task', '').replace('add todo', '').strip()
            if task:
                self.db.add_todo(task)
                return f"Task added: '{task}'"
            return "What task would you like me to add?"

        return None
