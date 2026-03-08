"""
Utility Tools: QR, Weather, Converter for v5.0
"""
import math

# --- QR Code ---
def generate_qr_stub(data):
    return f"QR Code generated for: {data}"

# --- Weather ---
def get_offline_weather_stub(location):
    return f"Offline weather forecast for {location}: Sunny, 25°C"

# --- Converter ---
def convert_units(value, from_unit, to_unit):
    # Simple example
    if from_unit == 'km' and to_unit == 'miles':
        return value * 0.621371
    if from_unit == 'celsius' and to_unit == 'fahrenheit':
        return (value * 9/5) + 32
    return f"Conversion from {from_unit} to {to_unit} not supported."
