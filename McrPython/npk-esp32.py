from machine import Pin, UART
import time

# Define RS485 pins for RE and DE to switch between transmit and receive mode
RS485_RE = 32
RS485_DE = 33

# Modbus RTU requests for reading NPK values
Com = bytearray([0x01, 0x03, 0x00, 0x1E, 0x00, 0x01, 0xE4, 0x0C])   # Command for Nitrogen (N)
Com1 = bytearray([0x01, 0x03, 0x00, 0x1F, 0x00, 0x01, 0xB5, 0xCC])  # Command for Phosphorus (P)
Com2 = bytearray([0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xC0])  # Command for Potassium (K)

# Setup UART communication
uart = UART(1, baudrate=9600, tx=17, rx=16, bits=8, parity=None, stop=1)

# Configure RE and DE pins as outputs
re_pin = Pin(RS485_RE, Pin.OUT)
de_pin = Pin(RS485_DE, Pin.OUT)

# Set RS485 module to receive mode initially
re_pin.value(0)
de_pin.value(0)

# CRC16 function for error-checking
def crc16(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 0x0001) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return ((crc & 0x00FF) << 8) | ((crc & 0xFF00) >> 8)

# Function to send command to the sensor
def send_command(command):
    re_pin.value(1)  # Set RS485 to transmit mode
    de_pin.value(1)
    uart.write(command)  # Send command
    time.sleep(0.01)
    re_pin.value(0)  # Set RS485 back to receive mode
    de_pin.value(0)

# Function to read response from the sensor
def read_response(length):
    timeout = 500
    start_time = time.ticks_ms()
    response = bytearray()
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
        if uart.any():
            response.extend(uart.read())
            if len(response) >= length:
                break
    return response

# General function to read NPK values
def read_value(command):
    send_command(command)
    response = read_response(7)  # Expecting 7 bytes in response
    if len(response) == 7 and response[1] == 0x03 and response[2] == 0x02:
        crc_received = (response[5] << 8) + response[6]
        crc_calculated = crc16(response[0:5])
        if crc_received == crc_calculated:
            value = (response[3] << 8) + response[4]
            return value
    return None

# Function to read Nitrogen (N) value
def read_n():
    return read_value(Com)

# Function to read Phosphorus (P) value
def read_p():
    return read_value(Com1)

# Function to read Potassium (K) value
def read_k():
    return read_value(Com2)

# Main loop to read and display NPK values
while True:
    N = read_n()
    P = read_p()
    K = read_k()
    
    print("N = {} mg/kg".format(N if N is not None else "Error"))
    print("P = {} mg/kg".format(P if P is not None else "Error"))
    print("K = {} mg/kg".format(K if K is not None else "Error"))

    time.sleep(1)  # Wait for 1 second before reading values again
