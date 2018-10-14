#!/usr/bin/python
import RPi.GPIO as GPIO
# set up the flag for ensure the PWM initilization once
left_start = False
right_start = False

# ===============================================
# Function of calculate the duty cycle and freq
# for certaion pulse width and intervals
# idle_period: the interval width
# pulse_period: the pulse width
# ===============================================
def cal_dc_and_freq(idle_period,pulse_period):
    dc = pulse_period / (pulse_period + idle_period) * 100
    freq = 1000 / (idle_period + pulse_period)
    return dc,freq

# pre-calculate the duty cycle and frequency for stop, clockwise and counterclkwise
idle_period = 20
stop_period = 0
fully_clockwise = 1.3
fully_counter_clockwise = 1.7
stop_dc,stop_freq = cal_dc_and_freq(idle_period,stop_period)
fully_clock_dc,fully_clock_freq = cal_dc_and_freq(idle_period,fully_clockwise)
fully_counter_dc,fully_counter_freq = cal_dc_and_freq(idle_period,fully_counter_clockwise)


# ================================================
# Function of change the frequency of left or right servo
# servo_number: 0 - left and 1 - right
# direction: the state of servo, stop, clkwise or counterclkwise
# ================================================
def servo_motion(servo_num,direction):
    if servo_num != 0 and servo_num!= 1:
        print "wrong servo num"
        os.exit(1)
        
    global left_start
    global right_start
    global p1
    global p2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(19,GPIO.OUT)
    
    if servo_num == 0:
        # only initialize the GPIO PWM once
        if left_start != True:
            p1 = GPIO.PWM(13,stop_freq)
            p1.start(stop_dc)
            left_start = True
        if direction == "clockwise":
            p1.ChangeFrequency(fully_clock_freq)
            p1.ChangeDutyCycle(fully_clock_dc)
        elif direction == "counterclockwise":
            p1.ChangeFrequency(fully_counter_freq)
            p1.ChangeDutyCycle(fully_counter_dc)
        elif direction == "idle":
            p1.ChangeFrequency(stop_freq)
            p1.ChangeDutyCycle(stop_dc)
    else:
        # only initialize the GPIO PWM once
        if right_start != True:
            p2 = GPIO.PWM(19,stop_freq)
            p2.start(stop_dc)
            right_start = True
        if direction == "clockwise":
            p2.ChangeFrequency(fully_clock_freq)
            p2.ChangeDutyCycle(fully_clock_dc)
        elif direction == "counterclockwise":
            p2.ChangeFrequency(fully_counter_freq)
            p2.ChangeDutyCycle(fully_counter_dc)
        elif direction == "idle":
            p2.ChangeFrequency(stop_freq)
            p2.ChangeDutyCycle(stop_dc)
    print servo_number, direction

# set up the GPIO mode
GPIO.setmode(GPIO.BCM)
# initialize the channels and some variables
channel = [17,22,23,27]
sub_channel=[17,22,23]
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
servo_number = 0
servo_dict = { '17':"clockwise", '22':"counterclockwise",'23':"idle"}
# Function of changing the servo state
def GPIO_callback(channel):
    servo_motion(servo_number,servo_dict[str(channel)])
#Function of switching the servo under control
def GPIO27_callback(channel):
    global servo_number
    servo_number = servo_number ^ 1
# Binding the callback function with GPIO pins
for chan in sub_channel:
    GPIO.add_event_detect(chan,GPIO.FALLING,callback=GPIO_callback,bouncetime=300)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback,bouncetime=300)
# waiting for Keyboard to interrupt the main process
try:
    while(1):
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()



