"""
Simple Health Monitor for v5.0
"""
import psutil
import time

class HealthMonitor:
    def get_stats(self):
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "uptime": time.time() # Simplified
        }
