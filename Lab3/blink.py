#!/usr/bin/python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)

p=GPIO.PWM(13,0.5)
p.start(50)
raw_input('Press return to stop:')
p.stop()
GPIO.cleanup()
