from sensors import npk, dth, light
import time
import network
import urequests

# Wi-Fi credentials (replace with your network's SSID and password)
WIFI_SSID = 'WLAN-45K2FB'
WIFI_PASSWORD = '51265629093004418224'

# API endpoint (replace <API_VM_IP_ADDRESS> with your API server's IP address)
API_URL = "http://192.168.2.212:5000/sensor-data"

# Function to connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)

    print("Connected to Wi-Fi")
    print("IP Address:", wlan.ifconfig()[0])

# Function to send data to the API
def send_data_to_api(payload):
    try:
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            print("Data sent successfully:", payload)
        else:
            print("Failed to send data. Status code:", response.status_code)

        response.close()
    except Exception as e:
        print("Error sending data to API:", e)

def main():
    connect_wifi()  # Connect to Wi-Fi before starting data transmission

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

        # Prepare payload for sending data to the API
        payload = {
            "N": n_value,
            "P": p_value,
            "K": k_value,
            "Temperature": temperature,
            "Humidity": humidity,
            "Lux": lux_value
        }

        # Send data to the API
        send_data_to_api(payload)

        # Wait for a few seconds before reading values again
        time.sleep(10)

if __name__ == "__main__":
    main()
