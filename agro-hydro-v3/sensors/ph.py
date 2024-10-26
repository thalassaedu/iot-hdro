from machine import ADC, Pin
from time import sleep

# Set up the ADC on pin 32
pH_pin = ADC(Pin(32))

# Configure the ADC attenuation (0db gives 0-1V range; adjust if needed)
pH_pin.atten(ADC.ATTN_11DB)  # 11dB attenuation provides a 0-3.3V input range

while True:
    # Read the analog value and convert it to voltage
    pH_value = pH_pin.read()  # Reads 0-4095
    voltage = pH_value * (3.3 / 4095.0)  # Scale to 3.3V for ESP32 ADC

    # Print the voltage to the serial console
    print(voltage)
    
    sleep(0.5)  # Delay for 500 ms
