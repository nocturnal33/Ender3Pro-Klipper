#!/usr/bin/python3

## Written by Nathan (nocturnal33)
## 2024.10.10

import requests
import time
import board
import neopixel
import signal
import sys
from setproctitle import setproctitle

## Set a process name for the script
setproctitle("neopixel_script")

###############
#### BOARD ####
###############
pixel_pin = board.D21

#################
#### PRINTER ####
#################
printer_ip = ''
RETRY_INTERVAL = 5

####################
#### LEDS STRIP ####
####################
ORDER = neopixel.GRB
total_pixels = 15
BRIGHTNESS_NORMAL = 0.6 # Normal brightness for heating
BRIGHTNESS_HIGH = 1.0   # Full brightness for printing

# Initialize with dim brightness
pixels = neopixel.NeoPixel(
    pixel_pin,
    total_pixels,
    brightness=BRIGHTNESS_NORMAL,
    auto_write=False,
    pixel_order=ORDER
)

################
#### COLORS ####
################
RED = (255, 0, 0)
GREEN = (0, 255, 0)
OFF = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)

###################
#### TEMP VARS ####
###################

TEMP_IDLE = 27      # Temperature below which printer is considered idle
TEMP_HEATING = 45  # Temperature above which printer is considered heating
TEMP_PRINTING = 60 # Temperature above which printer is considered printing

###################
#### FUNCTIONS ####
###################
def turn_off_pixels():
    """Turn off all pixels"""
    pixels.fill(OFF)
    pixels.show()

def signal_handler(sig, frame):
    """Handle graceful shutdown"""
    print('Turning off pixels and exiting...')
    turn_off_pixels()
    sys.exit(0)

def get_extruder_temperature(printer_ip, printer_port="80"):
    """Get printer temperature with improved error handling"""
    url = f"http://{printer_ip}:{printer_port}/printer/objects/query?extruder"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('result', {}).get('status', {}).get('extruder', {}).get('temperature')
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error getting temperature: {e}")
        return None

def set_all_pixels(color):
    """Set all pixels to a single color"""
    pixels.fill(color)
    pixels.show()

def chasing_effect(color, delay=0.05):
    """Create chasing effect"""
    for i in range(total_pixels):
        pixels[i] = color
        if i > 0:
            pixels[i - 1] = OFF
        pixels.show()
        time.sleep(delay)
    pixels[total_pixels - 1] = OFF
    pixels.show()

def check_connection(printer_ip, printer_port="80"):
    """Check printer connection status"""
    url = f"http://{printer_ip}:{printer_port}/printer/objects/query?extruder"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Connection error: {e}")
        return False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    """Main program loop"""
    if not printer_ip:
        print("Error: Printer IP address not configured")
        sys.exit(1)

    while True:
        if check_connection(printer_ip):
            temperature = get_extruder_temperature(printer_ip)

            if temperature is not None:
                et = float(temperature)
                print(f"Temperature is {et}°C")

                # Set brightness and behavior based on temperature
                if et < TEMP_IDLE:
                    # Idle state:
                    pixels.brightness = BRIGHTNESS_NORMAL
                    set_all_pixels(WHITE)
                elif TEMP_IDLE <= et < TEMP_PRINTING:
                    # Heating state: chasing red
                    pixels.brightness = BRIGHTNESS_HIGH
                    chasing_effect(RED)
                else:
                    # Printing state: bright white
                    pixels.brightness = BRIGHTNESS_HIGH
                    set_all_pixels(WHITE)
            else:
                print("Failed to retrieve temperature")
                pixels.brightness = BRIGHTNESS_NORMAL
                set_all_pixels(PURPLE)  # Purple indicates temperature read error
                time.sleep(1)
                turn_off_pixels()
                time.sleep(1)
        else:
            print(f"Connection failed. Retrying in {RETRY_INTERVAL} seconds...")
            pixels.brightness = BRIGHTNESS_NORMAL
            set_all_pixels(PURPLE)  # Purple indicates connection error
            time.sleep(2)
            turn_off_pixels()
            time.sleep(RETRY_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
        turn_off_pixels()
        sys.exit(1)
