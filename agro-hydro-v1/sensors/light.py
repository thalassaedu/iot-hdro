# sensors/light.py
from machine import Pin, I2C
from sensors.tsl2591 import TSL2591
import time

# Define the I2C pins for the TSL2591 sensor
SCL_PIN = 22  # GPIO pin for SCL
SDA_PIN = 21  # GPIO pin for SDA

# Initialize I2C communication and the TSL2591 sensor
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)  # Set I2C frequency to 100kHz for stability
tsl = TSL2591(i2c)  # Create TSL2591 sensor object

# Function to configure the sensor settings
def configure_sensor():
    print("Configuring TSL2591 sensor with optimal settings...")
    tsl.set_gain(0x10)  # Medium gain (25x) for improved sensitivity
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
        again = 25.0   # Gain multiplier (25x for medium gain)
        LUX_DF = 408.0  # Lux coefficient as per TSL2591 datasheet
        cpl = (atime * again) / LUX_DF  # Counts Per Lux calculation

        # Calculate lux using the formula: (Full Spectrum - Infrared) / CPL
        if cpl != 0:
            lux = (full_spectrum - infrared) / cpl
        else:
            lux = 0

        # Print intermediate values for debugging
        print(f"Debug: CPL: {cpl}, Calculated Lux: {lux}")
        return max(lux, 0)  # Return 0 if lux is negative or invalid

    except Exception as e:
        print(f"Failed to read from light sensor: {e}")
        return 0

# Configure the sensor with the updated settings
configure_sensor()
print("Light Sensor Test Starting...")
