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
python esptool.py --port /dev/tty.usbserial-0001 erase_flash
python esptool.py --port /dev/tty.usbserial-0001 --baud 115200 write_flash --flash_size=detect 0 esp8266-20210902-v1.17.bin
mpfshell -s full_upload.mpf
```
