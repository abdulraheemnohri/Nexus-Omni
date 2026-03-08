"""
Plugin Loader for v5.0
"""

import os
import importlib.util
import sys

class PluginLoader:
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir, exist_ok=True)
            return

        for folder in os.listdir(self.plugin_dir):
            plugin_path = os.path.join(self.plugin_dir, folder)
            if os.path.isdir(plugin_path) and not folder.startswith('__'):
                main_file = os.path.join(plugin_path, 'main.py')
                if os.path.exists(main_file):
                    self.load_plugin_file(folder, main_file)

    def load_plugin_file(self, name, file_path):
        try:
            spec = importlib.util.spec_from_file_location(name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the class that inherits from BasePlugin
            from modules.plugins.base_plugin import BasePlugin
            for attr in dir(module):
                cls = getattr(module, attr)
                if isinstance(cls, type) and issubclass(cls, BasePlugin) and cls is not BasePlugin:
                    plugin_instance = cls()
                    plugin_instance.initialize()
                    self.plugins[name] = plugin_instance
                    print(f"Loaded plugin: {name}")
                    break
        except Exception as e:
            print(f"Error loading plugin {name}: {e}")

    def get_plugin(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return [p.get_info() for p in self.plugins.values()]
