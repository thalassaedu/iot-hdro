from machine import Pin
from time import sleep

# Configure pin 32 as input
probe_pin = Pin(32, Pin.IN)

while True:
    # Read the digital value (0 or 1)
    probe_value = probe_pin.value()
    
    # Print the value to the console
    print("Probe Value:", probe_value)
    
    # Wait for a short period
    sleep(0.5)  # Adjust delay as needed
