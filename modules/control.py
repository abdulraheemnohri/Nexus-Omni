import subprocess
from modules.utils import get_logger

logger = get_logger("Control")

class ControlBridge:
    def __init__(self, config):
        self.config = config
        self.adb_ip = config['network']['adb_ip']

    def run_adb(self, cmd):
        # cmd should be a list of strings
        full_cmd = ["adb"] + cmd
        try:
            logger.info(f"Executing ADB: {' '.join(full_cmd)}")
            result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=10)
            return result.stdout
        except Exception as e:
            logger.error(f"ADB command failed: {e}")
            return str(e)

    def tap(self, x, y):
        return self.run_adb(["shell", "input", "tap", str(x), str(y)])

    def swipe(self, x1, y1, x2, y2, duration=500):
        return self.run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

    def start_app(self, package_name):
        return self.run_adb(["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"])

    def send_tasker_intent(self, command_name, extra_data=None):
        cmd = ["shell", "am", "broadcast", "-a", "com.nexus.COMMAND", "--es", "command", command_name]
        if extra_data:
            cmd += ["--es", "data", extra_data]
        return self.run_adb(cmd)

    def set_wifi(self, state):
        status = "enable" if state else "disable"
        return self.run_adb(["shell", "svc", "wifi", status])

    def capture_screen(self, filename="screen.png"):
        self.run_adb(["shell", "screencap", "-p", f"/sdcard/{filename}"])
        return self.run_adb(["pull", f"/sdcard/{filename}", filename])
