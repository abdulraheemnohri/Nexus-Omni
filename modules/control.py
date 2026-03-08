#!/usr/bin/env python3
"""
ADB Controller Module
"""

import subprocess
import logging

class ADBController:
    def __init__(self, adb_ip):
        self.adb_ip = adb_ip
        self.logger = logging.getLogger('ADB')

    def run_adb(self, cmd):
        full_cmd = ["adb"] + cmd
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=10)
            return result.stdout
        except Exception as e:
            self.logger.error(f"ADB Error: {e}")
            return str(e)

    def tap(self, x, y):
        return self.run_adb(["shell", "input", "tap", str(x), str(y)])

    def swipe(self, x1, y1, x2, y2, duration=500):
        return self.run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

    def send_intent(self, action, extras=None):
        cmd = ["shell", "am", "broadcast", "-a", action]
        if extras:
            for key, value in extras.items():
                cmd += ["--es", key, value]
        return self.run_adb(cmd)
