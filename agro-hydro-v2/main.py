# Import necessary modules
from sensors import npk, dth, light
import time

def main():
    while True:
        # Default values in case a sensor fails
        n_value, p_value, k_value = "N/A", "N/A", "N/A"
        temperature, humidity = "N/A", "N/A"
        lux_value = "N/A"

        try:
            # Attempt to read NPK sensor values
            n_value = npk.read_n() if npk.read_n() is not None else "N/A"
            p_value = npk.read_p() if npk.read_p() is not None else "N/A"
            k_value = npk.read_k() if npk.read_k() is not None else "N/A"
        except Exception as npk_error:
            print(f"Error reading NPK sensor: {npk_error}")

        try:
            # Attempt to read DHT sensor values
            temperature, humidity = dth.read_temperature_and_humidity()
            if temperature is None or humidity is None:
                temperature, humidity = "N/A", "N/A"
        except Exception as dht_error:
            print(f"Error reading DHT sensor: {dht_error}")

        try:
            # Attempt to read light sensor value
            lux_value = light.get_light_level()
            if lux_value is None:
                lux_value = "N/A"
        except Exception as light_error:
            print(f"Error reading light sensor: {light_error}")

        # Correct formatted print statement
        print(f"N: {n_value} mg/kg, P: {p_value} mg/kg, K: {k_value} mg/kg, "
              f"Temperature: {temperature} °C, Humidity: {humidity} %, "
              f"Lux: {lux_value}")

        # Wait for a few seconds before reading values again
        time.sleep(2)

if __name__ == "__main__":
    main()
