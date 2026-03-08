"""
Intruder Detection for v5.0
Captures photo on failed login attempt via Termux Camera API
"""
import subprocess
import datetime
import os

class IntruderDetection:
    def __init__(self, data_dir='data/security'):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def capture_photo(self, camera_id=0):
        """Capture photo from front camera"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        photo_path = os.path.join(self.data_dir, f'intruder_{timestamp}.jpg')

        try:
            # termux-camera-photo -c <id> <file>
            subprocess.run(['termux-camera-photo', '-c', str(camera_id), photo_path],
                         capture_output=True, text=True)
            return photo_path
        except Exception as e:
            print(f"Intruder capture error: {e}")
            return None

    def log_attempt(self, ip_address, username):
        """Log failed login attempt with metadata"""
        # Save IP and Timestamp to intruder log
        pass
