# sensors/light.py
from machine import Pin, I2C
from sensors.tsl2591 import TSL2591
import time

# Define I2C pins for TSL2591
SCL_PIN = 22  # GPIO pin for SCL
SDA_PIN = 21  # GPIO pin for SDA

# Initialize I2C communication and the TSL2591 sensor
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)  # Set I2C frequency to 100 kHz for stability
tsl = TSL2591(i2c)  # Create TSL2591 sensor object

# Function to configure the sensor settings
def configure_sensor():
    print("Configuring TSL2591 sensor...")
    tsl.set_gain(0x10)  # Medium gain (25x) for sensitivity in general environments
    tsl.set_integration_time(0x01)  # Integration time 200 ms for improved accuracy
    print("TSL2591 sensor configured successfully.")

# Function to calculate lux value accurately
def get_light_level():
    try:
        # Read the full spectrum and infrared values
        full_spectrum, infrared = tsl.get_full_luminosity()
        print(f"Debug: Full Spectrum: {full_spectrum}, Infrared: {infrared}")  # Print raw values for debugging

        # Calculate Counts Per Lux (CPL)
        integration_time_ms = 200.0  # Integration time in milliseconds
        gain = 25.0  # Gain multiplier for medium gain setting
        LUX_DF = 1032.9  # Adjusted Lux coefficient based on the latest analysis
        cpl = (integration_time_ms * gain) / LUX_DF

        # Calculate lux using dual equations
        if cpl != 0:
            lux1 = (full_spectrum - 1.64 * infrared) / cpl
            lux2 = (0.59 * full_spectrum - 0.86 * infrared) / cpl
            lux = max(lux1, lux2)  # Use the maximum value of both equations as the final lux value
        else:
            lux = 0

        print(f"Debug: CPL: {cpl}, Lux1: {lux1}, Lux2: {lux2}, Final Lux: {lux}")
        return max(lux, 0)  # Return 0 if lux is negative or invalid

    except Exception as e:
        print(f"Failed to read from light sensor: {e}")
        return 0

# Configure and initialize the sensor
configure_sensor()
print("Light Sensor Test Starting...")
