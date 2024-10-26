from machine import Pin
from time import sleep

# Change the pin to GPIO 27 (or another from the list)
probe_pin = Pin(27, Pin.IN)

while True:
    probe_value = probe_pin.value()
    print("Probe Value:", probe_value)
    sleep(0.5)
