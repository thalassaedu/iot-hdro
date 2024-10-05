# sensors/dth.py
import machine
import dht

dht_pin = machine.Pin(4)
sensor = dht.DHT11(dht_pin)

def read_temperature_and_humidity():
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        return temperature, humidity
    except OSError as e:
        print("Failed to read from DHT11 sensor, Error: ", e)
        return None, None
