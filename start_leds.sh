#!/bin/bash

source /home/pi/adafruit_env/bin/activate
sudo -E env "PATH=$PATH" python3 /home/pi/scripts/klipper_neopixel2.py
