# sensors/light.py
from machine import Pin, I2C
from sensors.tsl2591 import TSL2591
import time

# Define I2C pins for TSL2591
SCL_PIN = 22  # GPIO pin for SCL
SDA_PIN = 21  # GPIO pin for SDA

# Initialize I2C and TSL2591 sensor
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)  # Set I2C frequency to 100 kHz for stability
tsl = TSL2591(i2c)

# Function to configure the sensor settings
def configure_sensor():
    print("Configuring TSL2591 sensor with optimal settings...")
    # Use the correct gain and integration time for low light conditions
    tsl.set_gain(0x10)  # Set to Medium gain (25x)
    tsl.set_integration_time(0x01)  # Integration time 200ms for better accuracy
    print("TSL2591 sensor configured successfully.")

# Function to read and calculate lux value from the sensor
def get_light_level():
    try:
        # Read the full spectrum and infrared values
        full_spectrum, infrared = tsl.get_full_luminosity()
        print(f"Debug: Full Spectrum: {full_spectrum}, Infrared: {infrared}")  # Print raw values for debugging

        # Calculate Counts Per Lux (CPL) value based on integration time and gain
        atime = 200.0  # Integration time in ms
        again = 25.0  # Gain multiplier (25x for medium gain)
        cpl = (atime * again) / 408.0  # Adjust CPL based on the datasheet constant

        # Calculate lux based on sensor readings and CPL
        lux = tsl.calculate_lux(full_spectrum, infrared) if cpl != 0 else 0
        print(f"Debug: Calculated Lux: {lux}")  # Print calculated lux for debugging
        return max(lux, 0)  # Return 0 if lux is negative or invalid
    except Exception as e:
        print(f"Failed to read from light sensor: {e}")
        return 0

# Configure the sensor with the updated settings
configure_sensor()
print("Light Sensor Test Starting...")
