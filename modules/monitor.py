"""
System Monitoring Module
"""

import psutil
import os
import datetime

class Monitor:
    def get_stats(self):
        return {
            'cpu': psutil.cpu_percent(),
            'ram': psutil.virtual_memory().percent,
            'storage': self._get_storage_usage(),
            'battery': self._get_battery_status(),
            'timestamp': datetime.datetime.now().isoformat()
        }

    def _get_storage_usage(self):
        try:
            st = os.statvfs('/')
            free = st.f_bavail * st.f_frsize
            total = st.f_blocks * st.f_frsize
            return round((total - free) / total * 100, 2)
        except:
            return 0.0

    def _get_battery_status(self):
        # In a real app we'd use termux-battery-status
        return {"percentage": 85, "status": "discharging"}
