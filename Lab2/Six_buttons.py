#! /usr/bin/python
#========================================================
#  Name: Six_buttons.py
#  Date: 2018-09-20
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: Two
#  Description: This python script is used to control
#  all the buttons for PiTFT and two external buttons
#========================================================
import RPi.GPIO as GPIO
import time as time
#set up the mode for GPIO
GPIO.setmode(GPIO.BCM)
#initilize the GPIO pin numbers, the quit channel and the monitor frequency
chan_list = [17,22,23,27,13,19]
quit_chan = 27
quit_request = False
sleep_time_interval = 0.2
GPIO.setup(chan_list,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#loop for monitoring all the buttons unless the quit button is pressed
try:
    while True:
        if quit_request:
            print "The process will quit"
            break
        for channel in chan_list:
            if not GPIO.input(channel):
                print "Button %d has been pressed" % channel
                if channel == quit_chan:
                    quit_request = True
                    break
                time.sleep(sleep_time_interval)
except KeyboardInterrupt:
    GPIO.cleanup()
#clean up the GPIO
GPIO.cleanup()
