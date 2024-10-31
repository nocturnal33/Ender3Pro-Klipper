# Ender 3 Pro (OG Baby)
This is for a Creality Ender 3 Pro (2018) with an updated Creality 4.2.7 board and a CR Touch.
- stock fans
- stock hotend
- stock display

There is a neopixel 5v LED light strip controlled by the Raspberry Pi.

Light strip and Pi powered by Buck converter
Part for Rasperry Pi: 
https://www.thingiverse.com/thing:4586351

LED Scripts

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

LEDs are set to WHITE when heater gets above 50
It's in Python - adjust to your needs.




  

