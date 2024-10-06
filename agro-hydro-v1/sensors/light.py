# sensors/light.py
from machine import Pin, I2C
from sensors.tsl2591 import TSL2591  # Ensure tsl2591.py is in the sensors folder
import time

# Define the I2C pins for the TSL2591 sensor
SCL_PIN = 22  # SCL pin for I2C
SDA_PIN = 21  # SDA pin for I2C

# Initialize I2C communication for the TSL2591 sensor
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
tsl = TSL2591(i2c)  # Create TSL2591 sensor object

def configure_sensor():
    tsl.set_gain(0x00)  # Low gain (1x)
    tsl.set_integration_time(0x00)  # Integration time 100ms

def get_light_level():
    try:
        full_spectrum, infrared = tsl.get_full_luminosity()
        atime = 100.0  # Integration time in ms
        again = 1.0  # Gain multiplier
        cpl = (atime * again) / 408.0
        lux = tsl.calculate_lux(full_spectrum, infrared) if cpl != 0 else 0
        return max(lux, 0)  # Return 0 if lux is negative or invalid
    except Exception as e:
        print(f"Failed to read sensor data: {e}")
        return 0

# Initialize and configure the sensor
configure_sensor()
print("Light Sensor Test Starting...")
