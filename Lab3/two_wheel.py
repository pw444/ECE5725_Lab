#!/usr/bin/python

import RPi.GPIO as GPIO
left_start = False
right_start = False

def cal_dc_and_freq(idle_period,pulse_period):
    dc = pulse_period / (pulse_period + idle_period) * 100
    freq = 1000 / (idle_period + pulse_period)
    return dc,freq

def servo_motion(servo_num,direction):
    if servo_num != 0 and servo_num!= 1:
        print "wrong servo num"
        os.exit(1)

    idle_period = 20
    stop_period = 0
    fully_clockwise = 1.3
    fully_counter_clockwise = 1.7
    global left_start
    global right_start
    global p1
    global p2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(19,GPIO.OUT)
    still_dc,still_freq = cal_dc_and_freq(idle_period,stop_period)
    fully_clock_dc,fully_clock_freq = cal_dc_and_freq(idle_period,fully_clockwise)
    fully_counter_dc,fully_counter_freq = cal_dc_and_freq(idle_period,fully_counter_clockwise)

    if servo_num == 0:
        if left_start != True:
            p1 = GPIO.PWM(13,still_freq)
            p1.start(still_dc)
            left_start = True
        if direction == "clockwise":
            p1.ChangeFrequency(fully_clock_freq)
            p1.ChangeDutyCycle(fully_clock_dc)
        elif direction == "counterclockwise":
            p1.ChangeFrequency(fully_counter_freq)
            p1.ChangeDutyCycle(fully_counter_dc)
        elif direction == "idle":
            p1.ChangeFrequency(still_freq)
            p1.ChangeDutyCycle(still_dc)
    else:
        if right_start != True:
            p2 = GPIO.PWM(19,still_freq)
            p2.start(still_dc)
            right_start = True
        if direction == "clockwise":
            p2.ChangeFrequency(fully_clock_freq)
            p2.ChangeDutyCycle(fully_clock_dc)
        elif direction == "counterclockwise":
            p2.ChangeFrequency(fully_counter_freq)
            p2.ChangeDutyCycle(fully_counter_dc)
        elif direction == "idle":
            p2.ChangeFrequency(still_freq)
            p2.ChangeDutyCycle(still_dc)
    print servo_number, direction

GPIO.setmode(GPIO.BCM)
channel = [17,22,23,27]
sub_channel=[17,22,23]
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
servo_number = 0
servo_dict = { '17':"clockwise", '22':"counterclockwise",'23':"idle"}
def GPIO_callback(channel):
    servo_motion(servo_number,servo_dict[str(channel)])
def GPIO27_callback(channel):
    global servo_number
    servo_number = servo_number ^ 1
for chan in sub_channel:
    GPIO.add_event_detect(chan,GPIO.FALLING,callback=GPIO_callback,bouncetime=300)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback,bouncetime=300)
try:
    while(1):
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()



