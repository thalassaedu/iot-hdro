import tsl2591
import time
import RPi.GPIO as GPIO

# Pin definitions (use BCM mode for GPIO numbers)
INT_PIN = 25

# Initialize the TSL2591 sensor
sensor = tsl2591.Sensor()

# Interrupt flag
light_sensor_triggered = False

# Interrupt handler function
def light_sensor_isr(channel):
    global light_sensor_triggered
    light_sensor_triggered = True

# Configure the interrupt pin using RPi.GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set INT pin as input with pull-up resistor
GPIO.add_event_detect(INT_PIN, GPIO.FALLING, callback=light_sensor_isr)

# Function to display sensor details
def display_sensor_details():
    print("------------------------------------")
    print("Sensor:       TSL2591")
    print("Driver Ver:   Python")
    print("Unique ID:    2591")
    print("Max Value:    88,000 lux")
    print("Min Value:    0.0038 lux")
    print("Resolution:   0.001 lux")
    print("------------------------------------")

# Function to configure the sensor
def configure_sensor():
    # Set gain (low gain for high light levels)
    sensor.set_gain(tsl2591.GAIN_LOW)  # Low gain (1x)

    # Set integration time (shorter time for high light levels)
    sensor.set_timing(tsl2591.INTEGRATIONTIME_100MS)  # Medium integration time (100ms)

# Initialize the sensor and display details
display_sensor_details()
configure_sensor()
print("Light Sensor Test")

try:
    while True:
        # Check if the light sensor was triggered
        if light_sensor_triggered:
            # Clear the interrupt flag
            light_sensor_triggered = False

            # Read the sensor values
            full_spectrum, infrared = sensor.get_full_luminosity()
            lux = sensor.calculate_lux(full_spectrum, infrared)

            # Display the results
            if lux is not None:
                print(f"Full Spectrum (IR + Visible): {full_spectrum}")
                print(f"Infrared value: {infrared}")
                print(f"Visible value: {full_spectrum - infrared}")
                print(f"Lux: {lux} lux")
            else:
                print("Sensor overload or error")

        time.sleep(2)  # Wait for 2 seconds between readings

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()
    print("Program terminated")
