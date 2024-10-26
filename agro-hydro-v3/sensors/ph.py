from machine import ADC, Pin
from time import sleep

# Setup ADC on GPIO 32 for the pH sensor
pH_sensor = ADC(Pin(32))
pH_sensor.atten(ADC.ATTN_11DB)  # Set to 3.6V range

# Calibration constants
calibration_value = 21.34
sensitivity = -5.7

def read_voltage():
    # Take multiple readings to average out noise
    readings = [pH_sensor.read() for _ in range(10)]
    avg_reading = sum(readings) / len(readings)
    voltage = avg_reading / 4095 * 3.3
    return voltage

def check_sensor_state():
    voltage = read_voltage()
    # Calculate pH for reference (optional)
    pH_value = sensitivity * voltage + calibration_value
    
    # Print both the raw voltage and the pH value
    print(f"Voltage: {voltage:.2f}V, pH: {pH_value:.2f}")
    
    # Simple logic to differentiate between in water and out of water
    if voltage > 1.5:  # Voltage threshold to indicate "in water"
        print("Sensor is in water.")
    else:
        print("Sensor is out of water.")

while True:
    check_sensor_state()
    sleep(1)
