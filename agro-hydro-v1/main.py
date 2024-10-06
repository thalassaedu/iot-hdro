# main.py
from sensors import npk, dth, light
import time

def main():
    while True:
        # Read NPK values
        try:
            print("Reading NPK sensor values...")
            n_value = npk.read_n()
            p_value = npk.read_p()
            k_value = npk.read_k()
            print(f"N: {n_value} mg/kg, P: {p_value} mg/kg, K: {k_value} mg/kg")
        except Exception as e:
            print(f"Error reading NPK sensor: {e}")

        # Read temperature and humidity from DHT sensor
        try:
            print("Reading DHT sensor values...")
            temperature, humidity = dth.read_temperature_and_humidity()
            print(f"Temperature: {temperature} °C, Humidity: {humidity} %")
        except Exception as e:
            print(f"Error reading DHT sensor: {e}")

        # Read light level from light sensor (only every 10 seconds)
        try:
            print("Reading light sensor values...")
            light_level = light.get_light_level()
            print(f"Light Level: {light_level:.2f} lux")
        except Exception as e:
            print(f"Error reading light sensor: {e}")

        # Wait for a few seconds before the next reading
        print("Waiting for the next sensor reading...\n")
        time.sleep(3)  # Increased delay to avoid timing conflicts

if __name__ == "__main__":
    main()
