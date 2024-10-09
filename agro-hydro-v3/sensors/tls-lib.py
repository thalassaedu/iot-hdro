# // name of the file -tsl2591.py 
 # mpremote cp tsl2591.py :/tsl2591.py

# tsl2591.py - Custom TSL2591 driver for MicroPython

from machine import I2C

# I2C address for TSL2591
TSL2591_ADDR = 0x29

# Register and command codes
COMMAND_BIT = 0xA0
ENABLE_REG = 0x00
ENABLE_POWERON = 0x01
ENABLE_AEN = 0x02
CONTROL_REG = 0x01
CHAN0_LOW = 0x14
CHAN1_LOW = 0x16

# Gain and Integration time settings
GAIN_LOW = 0x00
INTEGRATIONTIME_100MS = 0x00

class TSL2591:
    def __init__(self, i2c, addr=TSL2591_ADDR):
        self.i2c = i2c
        self.addr = addr
        # Enable the sensor (power on and ALS enable)
        self._write_register(ENABLE_REG, ENABLE_POWERON | ENABLE_AEN)
        # Set default gain and integration time
        self.set_gain(GAIN_LOW)
        self.set_integration_time(INTEGRATIONTIME_100MS)

    def _write_register(self, reg, value):
        self.i2c.writeto_mem(self.addr, COMMAND_BIT | reg, bytes([value]))

    def _read_register(self, reg, length=2):
        return self.i2c.readfrom_mem(self.addr, COMMAND_BIT | reg, length)

    def set_gain(self, gain):
        control = self._read_register(CONTROL_REG, 1)[0]
        control &= 0xCF  # Clear previous gain setting
        control |= (gain & 0x30)
        self._write_register(CONTROL_REG, control)

    def set_integration_time(self, integration_time):
        control = self._read_register(CONTROL_REG, 1)[0]
        control &= 0xF8  # Clear previous integration time setting
        control |= (integration_time & 0x07)
        self._write_register(CONTROL_REG, control)

    def get_full_luminosity(self):
        # Read channel 0 and channel 1 values
        ch0 = self._read_register(CHAN0_LOW, 2)
        ch1 = self._read_register(CHAN1_LOW, 2)
        ch0 = ch0[1] << 8 | ch0[0]
        ch1 = ch1[1] << 8 | ch1[0]
        return ch0, ch1

    def calculate_lux(self, ch0, ch1):
        # Calculate lux based on sensor readings
        if ch0 == 0:
            return None
        if ch0 > 65535 or ch1 > 65535:
            return None

        # Calculate ratio of channels
        ratio = ch1 / ch0 if ch0 != 0 else 0
        # Determine lux calculation based on ratio (simplified formula)
        if ratio <= 0.5:
            lux = 0.0304 * ch0 - 0.062 * ch0 * (ratio ** 1.4)
        elif ratio <= 0.61:
            lux = 0.0224 * ch0 - 0.031 * ch1
        elif ratio <= 0.80:
            lux = 0.0128 * ch0 - 0.0153 * ch1
        elif ratio <= 1.30:
            lux = 0.00146 * ch0 - 0.00112 * ch1
        else:
            lux = 0
        return lux

    def clear_interrupt(self):
        # Clears any pending interrupts
        self._write_register(0xE7, 0x00)
