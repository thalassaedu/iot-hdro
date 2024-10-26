from machine import ADC, Pin
from time import sleep

# Setup ADC on GPIO 32
pH_sensor = ADC(Pin(32))
pH_sensor.atten(ADC.ATTN_11DB)  # 0-3.6V range

# Calibration constant based on known values
calibration_value = 20.24  # Adjust based on buffer solution calibration

def read_pH():
    buffer_arr = []
    for _ in range(10):  # Read multiple times to smooth out noise
        buffer_arr.append(pH_sensor.read())
        sleep(0.03)
    buffer_arr.sort()
    avg_value = sum(buffer_arr[2:8]) / 6  # Remove outliers and average the middle values
    voltage = avg_value / 4095 * 3.3  # Convert ADC reading to voltage
    pH_value = -5.70 * voltage + calibration_value  # Adjust with your calibration
    return pH_value

while True:
    pH = read_pH()
    print("pH Level:", pH)
    sleep(1)
