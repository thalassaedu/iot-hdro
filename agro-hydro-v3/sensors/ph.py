from machine import ADC, Pin
from time import sleep

# Setup the ADC for the pH sensor on GPIO 32
pH_sensor = ADC(Pin(32))  # Use GPIO 32 as the ADC pin
pH_sensor.atten(ADC.ATTN_11DB)  # Set attenuation to read up to 3.6V on ESP32 ADC

# Calibration constants - adjust these after calibration
offset = 0.0  # Offset obtained from calibration
slope = -5.7  # Adjust this slope based on calibration data

def read_pH():
    # Read raw analog value
    raw_value = pH_sensor.read()
    voltage = raw_value / 4095 * 3.3  # Convert raw value to voltage (0-3.3V for ESP32)

    # Convert voltage to pH value using calibration constants
    pH_value = slope * voltage + offset
    return pH_value

while True:
    pH = read_pH()
    print("pH Level:", pH)
    sleep(1)
