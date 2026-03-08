"""
Base Plugin Class for Nexus Omni v5.0
"""

class BasePlugin:
    def __init__(self, name, description, author="Nexus"):
        self.name = name
        self.description = description
        self.author = author
        self.enabled = False

    def initialize(self):
        """Called when plugin is loaded"""
        self.enabled = True
        print(f"Plugin {self.name} initialized.")

    def shutdown(self):
        """Called when plugin is unloaded"""
        self.enabled = False
        print(f"Plugin {self.name} shutdown.")

    def execute(self, command, args):
        """Main execution logic"""
        raise NotImplementedError("Plugins must implement execute()")

    def get_info(self):
        return {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "enabled": self.enabled
        }
