# sensors/light.py
from machine import Pin, I2C
from tsl2591 import TSL2591

INT_PIN = 25
SCL_PIN = 22
SDA_PIN = 21

i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
tsl = TSL2591(i2c)

def configure_sensor():
    tsl.set_gain(0x00)  
    tsl.set_integration_time(0x00)

def calculate_lux(ch0, ch1, cpl):
    if ch0 == 0:
        return None
    lux = (((0.8678 * float(ch0)) - float(ch1)) * (1.0 - (float(ch1) / float(ch0)))) / cpl
    return lux

def get_light_level():
    full_spectrum, infrared = tsl.get_full_luminosity()
    cpl = (100.0 * 1.0) / 408.0  
    lux = calculate_lux(full_spectrum, infrared, cpl)
    return lux if lux is not None else "Sensor overload or not reading correctly"
