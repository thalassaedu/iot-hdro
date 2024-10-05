import machine
import dht
import time
from machine import UART

# DHT Sensor Class
class DHTSensor:
    def __init__(self, pin_number):
        self.dht_pin = machine.Pin(pin_number)
        self.sensor = dht.DHT11(self.dht_pin)
        self.enabled = True  # By default, the sensor is enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def read(self):
        if not self.enabled:
            print("DHT sensor is disabled.")
            return None
        try:
            self.sensor.measure()
            temperature = self.sensor.temperature()
            humidity = self.sensor.humidity()
            return {"temperature": temperature, "humidity": humidity}
        except OSError as e:
            print("Failed to read from DHT sensor. Error: ", e)
            return None


# NPK Sensor Class
class NPKSensor:
    def __init__(self, rx_pin, tx_pin, re_pin, de_pin, baudrate=9600):
        self.uart = UART(1, baudrate=baudrate, rx=rx_pin, tx=tx_pin, timeout=1000)
        self.rs485_re = machine.Pin(re_pin, machine.Pin.OUT)
        self.rs485_de = machine.Pin(de_pin, machine.Pin.OUT)
        self.rs485_re.value(0)  # Set to receive mode
        self.rs485_de.value(0)  # Set to receive mode
        self.enabled = True  # By default, the sensor is enabled

        # Modbus RTU Commands
        self.Com = [0x01, 0x03, 0x00, 0x1E, 0x00, 0x01, 0xE4, 0x0C]   # Command for Nitrogen (N)
        self.Com1 = [0x01, 0x03, 0x00, 0x1F, 0x00, 0x01, 0xB5, 0xCC]  # Command for Phosphorus (P)
        self.Com2 = [0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xC0]  # Command for Potassium (K)

    def enable(self):
        self.enabled = True
        print("NPK sensor enabled.")

    def disable(self):
        self.enabled = False
        print("NPK sensor disabled.")

    def send_command(self, command):
        if not self.enabled:
            return  # Do nothing if sensor is disabled
        # Set RS485 to transmit mode
        self.rs485_re.value(1)
        self.rs485_de.value(1)
        self.uart.write(bytes(command))  # Send command via UART
        time.sleep(0.1)  # Short delay to ensure transmission is complete
        # Set RS485 back to receive mode
        self.rs485_re.value(0)
        self.rs485_de.value(0)

    def read_response(self, length):
        if not self.enabled:
            return []  # Return empty response if sensor is disabled
        # Read response from the sensor
        response = self.uart.read(length)
        if response is not None:
            return list(response)
        return []

    def calculate_crc(self, data):
        # CRC calculation for Modbus RTU
        crc = 0xFFFF
        for pos in range(len(data)):
            crc ^= data[pos]
            for _ in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        crc = ((crc & 0xFF) << 8) | ((crc >> 8) & 0xFF)
        return crc

    def read_value(self, command):
        if not self.enabled:
            return None  # Return None if sensor is disabled
        self.send_command(command)
        response = self.read_response(7)  # Expected response length
        if len(response) >= 7 and response[1] == 0x03 and response[2] == 0x02:
            # Verify CRC
            received_crc = (response[5] << 8) | response[6]
            calculated_crc = self.calculate_crc(response[:5])
            if received_crc == calculated_crc:
                return response[3] * 256 + response[4]  # Combine high and low bytes
        print("Error: Invalid response or CRC check failed.")
        return None

    def read_nitrogen(self):
        return self.read_value(self.Com)

    def read_phosphorus(self):
        return self.read_value(self.Com1)

    def read_potassium(self):
        return self.read_value(self.Com2)

    def read(self):
        if not self.enabled:
            print("NPK sensor is disabled.")
            return None
        n = self.read_nitrogen()
        p = self.read_phosphorus()
        k = self.read_potassium()
        return {"nitrogen": n, "phosphorus": p, "potassium": k}


# Sensor Manager Class
class SensorManager:
    def __init__(self):
        self.sensors = {}

    def add_sensor(self, sensor_name, sensor_obj):
        self.sensors[sensor_name] = sensor_obj

    def remove_sensor(self, sensor_name):
        if sensor_name in self.sensors:
            del self.sensors[sensor_name]

    def enable_sensor(self, sensor_name):
        if sensor_name in self.sensors:
            self.sensors[sensor_name].enable()
            print(f"{sensor_name} sensor enabled.")

    def disable_sensor(self, sensor_name):
        if sensor_name in self.sensors:
            self.sensors[sensor_name].disable()
            print(f"{sensor_name} sensor disabled.")

    def read_sensor(self, sensor_name):
        # Check if sensor is enabled before reading
        if sensor_name in self.sensors and self.sensors[sensor_name].enabled:
            return self.sensors[sensor_name].read()
        else:
            print(f"Sensor {sensor_name} is disabled or not found.")
            return None

    def read_all_sensors(self):
        readings = {}
        for sensor_name, sensor in self.sensors.items():
            if sensor.enabled:  # Read only from enabled sensors
                readings[sensor_name] = sensor.read()
        return readings

# Main Program
if __name__ == "__main__":
    # Initialize the Sensor Manager
    manager = SensorManager()

    # Create sensor instances
    dht_sensor = DHTSensor(pin_number=4)  # Replace 4 with your actual DHT GPIO pin number
    npk_sensor = NPKSensor(rx_pin=16, tx_pin=17, re_pin=32, de_pin=33)  # Replace with actual pins for RX, TX, RE, DE

    # Add sensors to the manager
    manager.add_sensor("DHT", dht_sensor)
    manager.add_sensor("NPK", npk_sensor)

    # Enable and read from sensors
    manager.enable_sensor("DHT")  # Enable DHT sensor
    #manager.disable_sensor("NPK")  # Disable NPK sensor
    manager.enable_sensor("NPK")

    while True:
        # Read and display sensor data
        dht_readings = manager.read_sensor("DHT")
        if dht_readings:
            print(f"DHT Readings: Temperature: {dht_readings['temperature']} °C, Humidity: {dht_readings['humidity']} %")

        npk_readings = manager.read_sensor("NPK")
        if npk_readings:
            print(f"NPK Readings: Nitrogen: {npk_readings['nitrogen']} mg/kg, Phosphorus: {npk_readings['phosphorus']} mg/kg, Potassium: {npk_readings['potassium']} mg/kg")

        # Wait for 2 seconds before the next reading
        time.sleep(2)
