# sensors/npk.py
from machine import Pin, UART
import time

RS485_RE = 32
RS485_DE = 33

Com = bytearray([0x01, 0x03, 0x00, 0x1E, 0x00, 0x01, 0xE4, 0x0C])  
Com1 = bytearray([0x01, 0x03, 0x00, 0x1F, 0x00, 0x01, 0xB5, 0xCC])  
Com2 = bytearray([0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xC0])  

uart = UART(1, baudrate=9600, tx=17, rx=16, bits=8, parity=None, stop=1)
re_pin = Pin(RS485_RE, Pin.OUT)
de_pin = Pin(RS485_DE, Pin.OUT)

re_pin.value(0)
de_pin.value(0)

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

def send_command(command):
    re_pin.value(1)
    de_pin.value(1)
    uart.write(command)
    time.sleep(0.01)
    re_pin.value(0)
    de_pin.value(0)

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

def read_value(command):
    send_command(command)
    response = read_response(7)
    if len(response) == 7 and response[1] == 0x03 and response[2] == 0x02:
        crc_received = (response[5] << 8) + response[6]
        crc_calculated = crc16(response[0:5])
        if crc_received == crc_calculated:
            value = (response[3] << 8) + response[4]
            return value
    return None

def read_n():
    return read_value(Com)

def read_p():
    return read_value(Com1)

def read_k():
    return read_value(Com2)
