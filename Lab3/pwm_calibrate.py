#!/usr/bin/python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)

pulse_period =1.5
idle_period = 20
frequency = 1000/(pulse_period + idle_period)
dc = pulse_period / (pulse_period + idle_period) * 100
print frequency
print dc
p=GPIO.PWM(13,frequency)
p.start(dc)
raw_input('Press return to stop:')
p.stop()
GPIO.cleanup()
