# Ender 3 Pro (OG Baby)
This is for a Creality Ender 3 Pro (2018) with an updated Creality 4.2.7 board and a CR Touch.
- stock fans
- stock hotend
- stock display

## Flash the printer
Put the .bin on an sd card, shut down printer, insert the sd card, turn on the printer and wait about 10 seconds.
Take out the SD card.


## Raspberry Pi
I am using a raspberry pi 3 that I had lying around
Printed Part for Rasperry Pi: 
https://www.thingiverse.com/thing:4586351

## LED Scripts
There is a neopixel 5v LED light strip controlled by the Raspberry Pi.
the LED strip is from Adafruit and slides into the tbe bottom of the top of the frame.



1. Use cron to start the LED scripts
```bash
@reboot /usr/bin/bash /home/pi/scripts/start_neopixel.sh >> /home/pi/scripts/neopixel.log 2>&1
```
2. Set up the Environment
```bash
sudo apt install python3-venv
python3 -m venv ~/adafruit_env
source ~/adafruit_env/bin/activate
pip3 install \
    Adafruit-Blinka \
    rpi_ws281x \
    adafruit-circuitpython-neopixel \
    requests \
    setproctitle RPi.GPIO
deactivate
```



3. LEDS
   LEDs are set to WHITE when heater gets above 50
   It's in Python - adjust to your needs.

Place the scripts in ~/scripts or modify the crontab to your new path

```bash
mkdir ~/scripts
```






  

