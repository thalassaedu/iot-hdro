from machine import ADC, Pin
from time import sleep

# Initialize ADC on GPIO 32
pH_sensor = ADC(Pin(32))
pH_sensor.atten(ADC.ATTN_11DB)  # 0-3.6V range for ESP32

# Calibration constants (adjust after calibration with buffer solutions)
calibration_value = 21.34  # Reference voltage for neutral pH 7
sensitivity = -5.7         # Slope for voltage to pH conversion

def read_pH():
    # Gather multiple readings to reduce noise
    readings = [pH_sensor.read() for _ in range(10)]
    readings.sort()
    avg_value = sum(readings[2:8]) / 6  # Average the middle values

    # Convert to voltage
    voltage = avg_value / 4095 * 3.3
    
    # Convert voltage to pH
    pH_value = sensitivity * voltage + calibration_value
    return pH_value

while True:
    pH = read_pH()
    print("pH Level:", pH)
    sleep(1)
