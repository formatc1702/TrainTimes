# Installation

```shell
# set up virtualenv
virtualenv venv/
source venv/bin/activate

# install utilities
pip install esptool          # for flashing ESP MCU
pip install mpfshell==0.9.1  # for uploading to ESP MCU
                             # (0.9.2 does not work)

# set up ESP MCU
cd firmware/traintimes-micropython
# esptool.py --port /dev/tty.usbserial-1410 erase_flash
esptool.py --port /dev/tty.usbserial-1410 erase_flash
# python esptool.py --port /dev/tty.usbserial-0001 --baud 115200 write_flash --flash_size=detect 0 esp8266-20210902-v1.17.bin
esptool.py --chip esp32 --port /dev/tty.usbserial-1410 --baud 115200 write_flash -z 0x1000 esp32-20210902-v1.17.bin
mpfshell -s full_upload.mpf

# monitor serial output
screen /dev/tty.usbserial-0001 115200  # to exit: press ctrl+A, type :quit, press Enter
```
