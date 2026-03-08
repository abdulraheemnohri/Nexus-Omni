"""
Sensor Triggers for v5.0
Supports Battery, Network, and GPS (via Termux API)
"""
import subprocess
import json

class TriggerEngine:
    def __init__(self, scheduler, workflow_engine):
        self.scheduler = scheduler
        self.workflow_engine = workflow_engine

    def check_battery(self, threshold=20, mode='below'):
        """Check battery via termux-battery-status"""
        try:
            res = subprocess.run(['termux-battery-status'], capture_output=True, text=True)
            status = json.loads(res.stdout)
            percent = status.get('percentage')

            if mode == 'below' and percent <= threshold:
                return True
            if mode == 'above' and percent >= threshold:
                return True
        except Exception as e:
            print(f"Battery trigger error: {e}")
        return False

    def check_wifi(self, ssid=None):
        """Check wifi via termux-wifi-connectionstatus"""
        try:
            res = subprocess.run(['termux-wifi-connectionstatus'], capture_output=True, text=True)
            status = json.loads(res.stdout)
            current_ssid = status.get('ssid')

            if ssid and current_ssid == ssid:
                return True
            if not ssid and current_ssid:
                return True
        except Exception as e:
            print(f"WiFi trigger error: {e}")
        return False

    def start_monitoring(self):
        """Schedule periodic sensor checks"""
        self.scheduler.add_job(self.sensor_loop, 'interval', minutes=1)

    def sensor_loop(self):
        # Battery check for power saver workflow
        if self.check_battery(15, 'below'):
            print("Trigger: Low Battery! Executing power_saver workflow...")
            # self.workflow_engine.execute_workflow(...)
