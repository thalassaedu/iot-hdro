from machine import ADC, Pin
from time import sleep
import array

# Calibration value for pH calculation
calibration_value = 21.34 - 0.7

# Initialize ADC on pin 32
pH_pin = ADC(Pin(32))
pH_pin.atten(ADC.ATTN_11DB)  # 11dB attenuation for 0-3.3V input range

# Buffer array to store pH readings
buffer_arr = array.array('i', [0] * 10)

def read_ph_value():
    global buffer_arr
    
    # Read 10 pH values with a short delay and store in buffer array
    for i in range(10):
        buffer_arr[i] = pH_pin.read()
        sleep(0.03)  # 30ms delay between readings
    
    # Sort the buffer array to eliminate extremes
    sorted_buffer = sorted(buffer_arr)
    
    # Calculate average of the middle 6 values
    avgval = sum(sorted_buffer[2:8]) / 6
    voltage = avgval * (3.3 / 4095.0)  # Convert to voltage for ESP32 ADC scale
    
    # Calculate pH value
    ph_act = -5.70 * voltage + calibration_value
    return ph_act

while True:
    # Read pH value and display it on the serial console
    ph_value = read_ph_value()
    print("pH Val:", ph_value)
    sleep(1)  # Delay of 1 second before the next reading
