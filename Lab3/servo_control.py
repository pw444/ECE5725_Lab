#!/usr/bin/python
#========================================================
#  Name: servo_control.py
#  Date: 2018-10-4
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: Three
#  Description: This python script is to change the pulse
#  width for servo to reach different speed and direction
#========================================================
import RPi.GPIO as GPIO
import time

# ==================================================
# Function of changing PWM freq and duty cycle
# step: the change step value for every iteration
# pulse_period: the width of pulse
# idle_period: the width of interval
# ===================================================
def frequency_change(step, pulse_period, idle_period):
    # the run time for each stage
    run_time = 3
    # the total iterations
    total_times = 10
    # use the value in main process
    global p
    for i in range(total_times):
        pulse_period=pulse_period+step
        new_frequency=1000/(pulse_period+idle_period)
        new_dc = pulse_period/ (pulse_period+ idle_period)*100
        p.ChangeFrequency(new_frequency)
        p.ChangeDutyCycle(new_dc)
        time.sleep(run_time)
        
        
# set up GPIO mode
GPIO.setmode(GPIO.BCM)
# set GPIO 13 as output port
GPIO.setup(13,GPIO.OUT)

# init the center pulse width and intervals
pulse_period = 1.5
idle_period = 20
# calculate the frequency and duty cycle for still state
frequency = 1000/(pulse_period + idle_period)
dc = pulse_period / (pulse_period + idle_period) * 100
# set the still state initially
p=GPIO.PWM(13,frequency)
p.start(dc)

# increase the speed of clockwise
frequency_change(-0.02, pulse_period, idle_period)

# reset the state for servo into still state
p.ChangeFrequency(frequency)
p.ChangeDutyCycle(dc)
pulse_period = 1.5
idle_period = 20

# increase the speed of counterclkwise
frequency_change(0.02, pulse_period, idle_period)

# set the servo to stop state
p.ChangeFrequency(frequency)
p.ChangeDutyCycle(0)

# wait for keyboard to stop the program
raw_input('Press return to stop:')
p.stop()
# clean up the GPIO 
GPIO.cleanup()
