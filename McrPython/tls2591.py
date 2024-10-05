from machine import Pin, I2C
import time
from tsl2591 import TSL2591

# Pin definitions
INT_PIN = 25
SCL_PIN = 22
SDA_PIN = 21

# Constants for improved lux calculation
GAIN_LOW = 0x00  # Low gain (1x)
INTEGRATIONTIME_100MS = 0x00  # Integration time for 100ms
TSL2591_LUX_DF = 408.0  # Adjusted constant for more accurate lux calculation

# Initialize I2C
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)

# Perform I2C scan to check connected devices
devices = i2c.scan()
if 0x29 not in devices:
    raise Exception("TSL2591 not detected on the I2C bus.")

# Initialize the TSL2591 sensor
tsl = TSL2591(i2c)

# Function to configure the sensor
def configure_sensor():
    print("Configuring sensor with low gain and 100ms integration time...")
    tsl.set_gain(GAIN_LOW)  # Low gain (1x)
    tsl.set_integration_time(INTEGRATIONTIME_100MS)  # Medium integration time (100ms)
    print("Sensor configured successfully.")

# Improved function for lux calculation
def calculate_lux(ch0, ch1, cpl):
    if ch0 == 0:  # Prevent division by zero
        return None
    lux = (((0.8678 * float(ch0)) - float(ch1)) * (1.0 - (float(ch1) / float(ch0)))) / cpl
    return lux

# Initialize the sensor and configure settings
configure_sensor()
print("Light Sensor Test Starting...")

# Calculate CPL (Counts Per Lux) value based on integration time and gain
atime = 100.0  # Integration time in ms
again = 1.0  # Gain multiplier (1x for low gain)
cpl = (atime * again) / TSL2591_LUX_DF

while True:
    try:
        # Read sensor values
        full_spectrum, infrared = tsl.get_full_luminosity()
        print(f"Full Spectrum: {full_spectrum}, Infrared: {infrared}")  # Debug print

        # Calculate and display lux using the improved formula
        lux = calculate_lux(full_spectrum, infrared, cpl)
        if lux is not None:
            print(f"Light Level: {lux:.2f} lux")
        else:
            print("Sensor overload or not reading correctly")

    except Exception as e:
        print(f"Failed to read sensor data: {e}")

    time.sleep(2)  # Wait for 2 seconds between readings
