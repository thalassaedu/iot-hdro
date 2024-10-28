from machine import ADC, Pin
import time

# Setup
ph_pin = 32  # Use the ADC pin connected to the pH sensor
adc = ADC(Pin(ph_pin))
adc.atten(ADC.ATTN_11DB)  # Configure for the full 0-3.3V range
adc.width(ADC.WIDTH_12BIT)  # Use 12-bit resolution (0-4095)

# Calibration values (voltage to pH)
# Adjust based on your calibration solutions
voltage_at_ph7 = 1500  # midpoint for pH 7
voltage_per_ph_unit = 59.16  # estimated slope (mV per pH unit)

def read_ph():
    # Read sensor voltage
    voltage = adc.read() * (3.3 / 4095.0) * 1000  # Convert to mV
    # Calculate pH from the voltage
    ph_value = 7.0 - ((voltage - voltage_at_ph7) / voltage_per_ph_unit)
    return round(ph_value, 2)

while True:
    ph = read_ph()
    print("pH Value:", ph)
    time.sleep(1)  # Wait for 1 second before the next reading
