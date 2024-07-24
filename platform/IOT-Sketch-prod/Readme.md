# This readme file contain all the sesnsor connections
## Light sensor connection with arduino -
 - Light sensor has 4 pins
    - INT --> Digital 5 
    - SCL --> Analog A5
    - SDA --> Analog A4
    - GND --> GND
    - VCC --> V5
- Code is inside --> /Users/D073341/work/sre-cops/iot-hdro/platform/IOT-Sketch-prod/Light-Arduino 

## DTH Sensor
    - Data pin --> Digital 6
    - Code - /Users/D073341/work/sre-cops/iot-hdro/platform/IOT-Sketch-prod/temp-humidy-sketch

## Soil moisture 
    - Board 
    - On two pin side, where the "L" is mentioned is "-" and other is +
    - "L -" will connect to probe on "right" side where it has wrtten in chinese. 
    - and "+" will connect to the left side.
    - A0 --> Arduino A0(D0 not connected). 
    - Code --> /Users/D073341/work/sre-cops/iot-hdro/platform/IOT-Sketch-prod/temp-humidy-sketch
    -- Now plan is to connect with ESP32.
        ESP -
            Data pin to each sensor :
                Sensor1 --> G34
                Sensor2 --> G35
                Sensor3 --> G32
                Sensor4 --> G33
                Sensor5 --> G25
                vcc -3v - not to 5v