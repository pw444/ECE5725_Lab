#!/usr/bin/python
import RPi.GPIO as GPIO
# set up GPIO mode
GPIO.setmode(GPIO.BCM)
# set GPIO 13 for output port
GPIO.setup(13,GPIO.OUT)
# init the blink frequency
freq = 0.5
# set the PWM frequency
p=GPIO.PWM(13,freq)
# set duty cycle
p.start(50)
# waiting for keyboard to stop the program
raw_input('Press return to stop:')
p.stop()
# clean up the GPIO 
GPIO.cleanup()
