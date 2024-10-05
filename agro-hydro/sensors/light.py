# sensors/light.py
from machine import Pin, I2C
from sensors.tsl2591 import TSL2591
import time

# Pin definitions for I2C and interrupt
INT_PIN = 25
SCL_PIN = 22
SDA_PIN = 21

# Initialize I2C and sensor
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
tsl = TSL2591(i2c)

# Function to configure the sensor
def configure_sensor():
    tsl.set_gain(TSL2591.GAIN_LOW)  # Set to low gain (1x)
    tsl.set_integration_time(TSL2591.INTEGRATIONTIME_100MS)  # Set integration time to 100ms
    print("Sensor configured successfully.")

# Improved function for lux calculation
def calculate_lux(ch0, ch1, cpl):
    # If no light is detected, return 0 lux directly
    if ch0 == 0 or ch1 == 0:
        return 0
    # Calculate lux based on sensor values
    lux = (((0.8678 * float(ch0)) - float(ch1)) * (1.0 - (float(ch1) / float(ch0)))) / cpl
    return max(lux, 0)  # Ensure lux is not negative

# Function to get light level in lux
def get_light_level():
    try:
        # Read sensor values
        full_spectrum, infrared = tsl.get_full_luminosity()
        print(f"Debug: Full Spectrum: {full_spectrum}, Infrared: {infrared}")

        # Calculate CPL (Counts Per Lux) value based on integration time and gain
        atime = 100.0  # Integration time in ms
        again = 1.0  # Gain multiplier (1x for low gain)
        cpl = (atime * again) / 408.0

        # Calculate lux and handle low light scenario
        lux = calculate_lux(full_spectrum, infrared, cpl)
        if lux == 0:
            return 0  # Return 0 lux when no light detected
        return lux
    except Exception as e:
        # Instead of returning 0 on error, print and re-raise the exception
        print(f"Failed to read sensor data: {e}")
        raise  # Re-raise the exception for error handling elsewhere

# Initialize and configure the sensor
configure_sensor()
print("Light Sensor Test Starting...")

# Loop to continuously read and display lux value
while True:
    try:
        light_level = get_light_level()
        print(f"Light Level: {light_level:.2f} lux")
    except Exception as error:
        print(f"Error reading light sensor: {error}")  # Report sensor read error
    time.sleep(2)  # Wait 2 seconds before the next reading
