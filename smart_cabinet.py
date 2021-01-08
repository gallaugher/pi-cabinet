# smart_cabinet.py by John Gallaugher - @gallaugher, youtube.com/profgallaugher
# Step-by-step build instructions, link to project build tutorial video, and a
# sample parts list can be found at:
# gallaugher.com/pi-cabinet
# 
# The Smart Cabinet is meant as a reminder to take vitamins or medications.
# It is a demonstration product, not a medical device. No warranty is intended
# or implied with this project and the author is not liable for any harm that
# might come from use, misuse, software or hardware failure, or for any other reason.
#
# If the project is built according to specs at: gallaugher.com/pi-cabinet
# an LED will flash when this code is first run to show the device is active.
# Opening and closing the device door will turn off the LED.
# The LED will light again at any time included in the alarm_times list.
# Opening the cabinet door will again turn off the LED light until the next
# time in the alarm_times list is reached.
# alarm_times must be listed in 24 hr. time.
# This code uses CircuitPython on a Wi-Fi capable Raspberry Pi and 
# was tested on a Raspberry Pi WH running Raspberry OS in early 2021.
# The magnetic contact switch (door sensor) is attached to pin D23
# The LED is attached to pin D24.
# 
# Code can be scheduled to run when the Pi is powered up by using:
# sudo crontab -e
# then entering the following at the bottom:
# @reboot python3 door_sensor.py &

import schedule
import subprocess
import time
import board
import digitalio

# set up door sensor
door_sensor = digitalio.DigitalInOut(board.D23)
door_sensor.direction = digitalio.Direction.INPUT
door_sensor.pull = digitalio.Pull.UP
led = digitalio.DigitalInOut(board.D24)
led.direction = digitalio.Direction.OUTPUT
led.value = True
# flash LED when program is first run.
flash = True

# WARNING: BE SURE to use 24 hr. time in single quotes
# e.g. '00:00' is midnight, '12:00' is noon, '11:00' is 11am, '23:59' is 11:59 pm
alarm_times = ['05:00', '17:00', '22:00']

# get and print the local time, just so you can be sure your Pi's timezone is set
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print('current time:' + current_time)

def job():
    led.value = True # turn light on

# schedules job above to turn light on for each of the alarm_times
for alarm_time in alarm_times:
    schedule.every().day.at(alarm_time).do(job)
    print('scheduled :' + alarm_time)

while True:
    # flash is True when program first runs.
    # Useful to let user know program is running or if power went out and
    # system restarted since the door was last opened
    if flash:
        led.value = not led.value
        time.sleep(0.5)
        if door_sensor.value: # if door is opened
            print("- STOP FLASH!!")
            led.value = False # turn off the LED
            flash = False # and stop flashing
    else: # light isn't flashing, so light is steady at any alarm_times
        schedule.run_pending()
        if door_sensor.value:
            print("*** DOOR OPEN!")
            led.value = False
        else:
            print("DOOR CLOSED")
        time.sleep(0.5)
