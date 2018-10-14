#!/usr/bin/python
import RPi.GPIO as GPIO
# set up GPIO mode
GPIO.setmode(GPIO.BCM)
# set GPIO 13 as output port
GPIO.setup(13,GPIO.OUT)

# calculate the frequency and duty cycle
pulse_period =1.5
idle_period = 20
frequency = 1000/(pulse_period + idle_period)
dc = pulse_period / (pulse_period + idle_period) * 100

# init GPIO PWM output
p=GPIO.PWM(13,frequency)
p.start(dc)
# wait for keyboard to stop the program
raw_input('Press return to stop:')
p.stop()
# clean up the GPIO
GPIO.cleanup()
