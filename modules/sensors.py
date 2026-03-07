#!/usr/bin/env python3
"""
Sensor Fusion Module
"""

import subprocess
import json

class SensorFusion:
    def get_battery(self):
        try:
            # Mock for sandbox
            return {"percentage": 85, "status": "discharging"}
        except:
            return {"percentage": 100}

    def get_location(self):
        return {"lat": 0.0, "lon": 0.0}
