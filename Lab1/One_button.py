#! /usr/bin/python
#========================================================
#  Name: One_button.py
#  Date: 2018-09-09
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: One
#  Description: This python script is used to control
#  the GPIO #17 for PiTFT
#========================================================
import RPi.GPIO as GPIO
import time as time
#set the mode for GPIO
GPIO.setmode(GPIO.BCM)
#initialize the GPIO #17
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#obtain the current time
ctime = time.time()
#loop for monitoring the GPIO #17 unless no reaction after 5 seconds
while time.time() - ctime < 5:
    if not GPIO.input(17):
        print 'Button 17 has been pressed'
        time.sleep(1)
        ctime = time.time()
#clean up the GPIO
GPIO.cleanup()

