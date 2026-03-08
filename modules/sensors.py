#!/usr/bin/env python3
"""
Sensor Fusion Module
"""

import subprocess
import json

import os

class SensorFusion:
    def _run_termux_api(self, command):
        try:
            result = subprocess.run([command], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass
        return {}

    def get_battery(self):
        return self._run_termux_api("termux-battery-status")

    def get_location(self):
        return self._run_termux_api("termux-location")

    def get_wifi(self):
        return self._run_termux_api("termux-wifi-connectioninfo")

    def get_system_stats(self):
        stats = {
            "ram": self._get_ram_usage(),
            "cpu": self._get_cpu_usage(),
            "storage": self._get_storage_usage()
        }
        return stats

    def _get_ram_usage(self):
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                total = int(lines[0].split()[1])
                free = int(lines[1].split()[1])
                return round((total - free) / total * 100, 2)
        except:
            return 0.0

    def _get_cpu_usage(self):
        try:
            return round(float(os.popen("top -n 1 -b | grep 'CPU:' | awk '{print $2}' | cut -d% -f1").read()), 2)
        except:
            return 0.0

    def _get_storage_usage(self):
        try:
            st = os.statvfs('/')
            free = st.f_bavail * st.f_frsize
            total = st.f_blocks * st.f_frsize
            used = (total - free)
            return round(used / total * 100, 2)
        except:
            return 0.0
