# main.py
from sensors import npk, dth, light

def main():
    # Read NPK values
    n_value = npk.read_n()
    p_value = npk.read_p()
    k_value = npk.read_k()
    print(f"N: {n_value} mg/kg, P: {p_value} mg/kg, K: {k_value} mg/kg")

    # Read temperature and humidity
    temperature, humidity = dth.read_temperature_and_humidity()
    print(f"Temperature: {temperature} °C, Humidity: {humidity} %")

    # Read light level
    light_level = light.get_light_level()
    print(f"Light Level: {light_level} lux")

if __name__ == "__main__":
    main()
