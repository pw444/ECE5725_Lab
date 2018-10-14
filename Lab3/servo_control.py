#!/usr/bin/python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)

def frequency_change(step, pulse_period, idle_period):
    ctime = time.time()
    for i in range(10):
        while time.time() - ctime < 3:
            pass
        pulse_period=pulse_period+step
        new_frequency=1000/(pulse_period+idle_period)
        new_dc = pulse_period/ (pulse_period+ idle_period)*100
        p.ChangeFrequency(new_frequency)
        p.ChangeDutyCycle(new_dc)
        print new_dc
        ctime = time.time()

pulse_period =1.5
idle_period = 20
frequency = 1000/(pulse_period + idle_period)
dc = pulse_period / (pulse_period + idle_period) * 100
print dc
global p
p=GPIO.PWM(13,frequency)
p.start(dc)
frequency_change(-0.02, pulse_period, idle_period)

p.ChangeFrequency(frequency)
p.ChangeDutyCycle(dc)
pulse_period =1.5
idle_period = 20

frequency_change(0.02, pulse_period, idle_period)

p.ChangeFrequency(frequency)
p.ChangeDutyCycle(0)



raw_input('Press return to stop:')
p.stop()
GPIO.cleanup()
