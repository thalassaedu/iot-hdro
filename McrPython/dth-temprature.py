import machine
import dht
import time

# Define the GPIO pin where the DHT11 sensor is connected.
dht_pin = machine.Pin(4)

# Create an instance of the DHT class using the DHT11 sensor.
sensor = dht.DHT11(dht_pin)

# Initialize serial communication (optional for debugging, ESP32 uses REPL).
print("DHT11 Sensor Test")

# Infinite loop to continuously read and display sensor data.
while True:
    try:
        # Read the temperature and humidity from the DHT11 sensor.
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Display the current temperature and humidity.
        print("Temperature: {} °C\tHumidity: {} %".format(temperature, humidity))

    except OSError as e:
        # Print error message if sensor reading fails.
        print("Failed to read from DHT11 sensor, Error: ", e)

    # Wait for 2 seconds before taking another reading.
    time.sleep(2)
