# To flash micropython inside esp32 using resberry pi

    - Install python on resberry pi(It usally installed defaul).
        python3 --version
    
    - Enable virtual environment on Python
        pip install virtualenv
        python3 -m mvvenv venv
        In my case - source iot/bin/activate
        source myvenv?bin?activated
    
    - After enabling virtual environment, install esptool module.
        pip3 install esptool
        wget https://micropython.org/resources/firmware/ESP32_GENERIC-20240222-v1.22.2.bin

    - Flash the esp32
        esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
        esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20240222-v1.22.2.bin
    - Install mpremote to upload pyhton based program in esp32
        pip3 install mpremote
    - Connect mpremote and upload python code
        mpremote connect /dev/ttyUSB0 fs cp main.py :
        mpremote connect /dev/ttyUSB0 exec "import main"
