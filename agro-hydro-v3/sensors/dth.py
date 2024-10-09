# sensors/dth.py
import machine
import dht
import time

# Define the GPIO pin where the DHT11 sensor is connected.
DHT_PIN = 4  # Change this to the actual GPIO pin number, if different

# Create an instance of the DHT class using the DHT11 sensor.
sensor = dht.DHT11(machine.Pin(DHT_PIN))

def read_temperature_and_humidity():
    try:
        print("Reading temperature and humidity from DHT sensor...")
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        print(f"Temperature: {temperature} °C, Humidity: {humidity} %")  # Debug print
        return temperature, humidity
    except OSError as e:
        print(f"Failed to read from DHT11 sensor, Error: {e}")
        return None, None
