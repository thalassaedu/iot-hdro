# main.py
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
            print("Error reading NPK sensor: {}".format(npk_error))

        try:
            # Attempt to read DHT sensor values
            temperature, humidity = dth.read_temperature_and_humidity()
            if temperature is None or humidity is None:
                temperature, humidity = "N/A", "N/A"
        except Exception as dht_error:
            print("Error reading DHT sensor: {}".format(dht_error))

        try:
            # Attempt to read light sensor value
            lux_value = light.get_light_level()
            if lux_value is None:
                lux_value = "N/A"
        except Exception as light_error:
            print("Error reading light sensor: {}".format(light_error))

        # Correct formatted print statement using .format()
        print("N: {} mg/kg, P: {} mg/kg, K: {} mg/kg, Temperature: {} °C, Humidity: {} %, Lux: {}".format(
              n_value, p_value, k_value, temperature, humidity, lux_value))

        # Wait for a few seconds before reading values again
        time.sleep(2)

if __name__ == "__main__":
    main()
