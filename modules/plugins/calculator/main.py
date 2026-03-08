"""
Calculator Plugin Sample
"""
from modules.plugins.base_plugin import BasePlugin

class CalculatorPlugin(BasePlugin):
    def __init__(self):
        super().__init__(
            name="Calculator",
            description="Performs basic arithmetic operations.",
            author="Nexus Team"
        )

    def execute(self, command, args):
        if command == "add":
            return sum(args)
        elif command == "multiply":
            res = 1
            for x in args: res *= x
            return res
        return "Unknown calculator command"
