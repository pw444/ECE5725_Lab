#!/usr/bin/python

import sys
import getopt as opt
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO
import os
import time
left_start = False
right_start = False

def cal_dc_and_freq(idle_period,pulse_period):
    dc = pulse_period / (pulse_period + idle_period) * 100
    freq = 1000 / (idle_period + pulse_period)
    return dc,freq

idle_period = 20
stop_period = 0
fully_clockwise = 1.3
fully_counter_clockwise = 1.7
still_dc,still_freq = cal_dc_and_freq(idle_period,stop_period)
fully_clock_dc,fully_clock_freq = cal_dc_and_freq(idle_period,fully_clockwise)
fully_counter_dc,fully_counter_freq = cal_dc_and_freq(idle_period,fully_counter_clockwise)

def servo_motion(servo_num,direction):
    if servo_num != 0 and servo_num!= 1:
        print "wrong servo num"
        os.exit(1)
    global left_start
    global right_start
    global p1
    global p2
    global still_dc
    global still_freq
    global fully_clock_dc
    global fully_clock_freq
    global fully_counter_dc
    global fully_counter_freq

    if servo_num == 0:
        if left_start != True:
            p1 = GPIO.PWM(13,still_freq)
            p1.start(still_dc)
            left_start = True
        if direction == "clkwise":
            p1.ChangeFrequency(fully_clock_freq)
            p1.ChangeDutyCycle(fully_clock_dc)
        elif direction == "counterclk":
            p1.ChangeFrequency(fully_counter_freq)
            p1.ChangeDutyCycle(fully_counter_dc)
        elif direction == "stop":
            p1.ChangeFrequency(still_freq)
            p1.ChangeDutyCycle(still_dc)
    else:
        if right_start != True:
            p2 = GPIO.PWM(19,still_freq)
            p2.start(still_dc)
            right_start = True
        if direction == "clkwise":
            p2.ChangeFrequency(fully_clock_freq)
            p2.ChangeDutyCycle(fully_clock_dc)
        elif direction == "counterclk":
            p2.ChangeFrequency(fully_counter_freq)
            p2.ChangeDutyCycle(fully_counter_dc)
        elif direction == "stop":
            p2.ChangeFrequency(still_freq)
            p2.ChangeDutyCycle(still_dc)
    print servo_number, direction

#class for font button
class My_font:
    def __init__(self, text, color, pos, size = 40):
        self.font = pygame.font.Font(None, size)
        self.text_surface = self.font.render(text,True,color)
        self.rect = self.text_surface.get_rect(center = pos)


#switch the mode of display
display_on_piTFT = False
try:
    opts, args = opt.getopt(sys.argv[1:], "P")
    for o,a in opts:
        if o in ("-P", ):
            display_on_piTFT = True
except opt.GetoptError:
    print 'The error occurs in arguments'
    exit(1)
	
if display_on_piTFT:
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb1') 
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

def dict_change(servo_num, direction):
    ctime = time.time()
    global stime
    global left_history_info
    global right_history_info
    if(servo_num == 0):
        left_history_info[(60,140)] = left_history_info[(60,120)]
        left_history_info[(60,120)] = left_history_info[(60,100)]
        left_history_info[(60,100)] = '{:<10}'.format(direction) +  str(int(ctime-stime))
    else:
        right_history_info[(260,140)] = right_history_info[(260,120)]
        right_history_info[(260,120)] = right_history_info[(260,100)]
        right_history_info[(260,100)] = '{:<10}'.format(direction) +  str(int(ctime-stime))


running = True
is_start = False
is_stop = False
re_draw = False

GPIO.setmode(GPIO.BCM)
out_channel=[13,19]
GPIO.setup(out_channel, GPIO.OUT)
servo_number = 0
servo_dict = { '17':"clkwise", '22':"counterclk",'23':"stop"}
def state_change(state):
    global re_draw
    global is_stop
    global latest_left
    global latest_right
    if is_stop == False:
        re_draw = True
        if state == 2:
            servo_motion(0,'clkwise')
            servo_motion(1,'counterclk')
            latest_left = 'clkwise'
            latest_right = 'counterclk'
            dict_change(0,'clkwise')
            dict_change(1,'counterclk')
        elif state == 0:
            servo_motion(0,'counterclk')
            servo_motion(1,'clkwise')
            latest_left = 'counterclk'
            latest_right = 'clkwise'
            dict_change(0,'counterclk')
            dict_change(1,'clkwise')
        elif state == 3:
            servo_motion(0,'stop')
            servo_motion(1,'clkwise')
            latest_left = 'stop'
            latest_right = 'clkwise'
            dict_change(0,'stop')
            dict_change(1,'clkwise')
        elif state == 5:
            servo_motion(0,'counterclk')
            servo_motion(1,'stop')
            latest_left = 'counterclk'
            latest_right = 'stop'
            dict_change(0,'counterclk')
            dict_change(1,'stop')
        else:
            servo_motion(0,'stop')
            servo_motion(1,'stop')
            latest_left = 'stop'
            latest_right = 'stop'
            dict_change(0,'stop')
            dict_change(1,'stop')


pygame.init()
if display_on_piTFT:
    pygame.mouse.set_visible(False)
else:
    pygame.mouse.set_visible(True)
size = width,height = 320,240
black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0
screen = pygame.display.set_mode(size)
screen.fill(black)
main_font = pygame.font.Font(None, 25)

#render quit button
start = My_font('start',white,(70,210))
quit = My_font('quit',white,(250,210))
stop = My_font('stop',white,(160,120),30)
resume = My_font('resume',white,(160,120),30)
left_history = My_font('left history',white,(60,60),25)
right_history = My_font('right history',white,(260,60),25)
left_history_info = { (60,100):'stop         0', (60,120):'stop         0', (60,140):'stop         0'}
right_history_info = { (260,100):'stop         0', (260,120):'stop         0', (260,140):'stop         0'}

circle_rect = pygame.draw.circle(screen, red, [160, 120], 35)
screen.blit(start.text_surface,start.rect)
screen.blit(quit.text_surface,quit.rect)
screen.blit(stop.text_surface,stop.rect)
screen.blit(left_history.text_surface,left_history.rect)
screen.blit(right_history.text_surface,right_history.rect)
for text_pos, my_text in left_history_info.items():
    text_surface = main_font.render(my_text, True, white)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)
for text_pos, my_text in right_history_info.items():
    text_surface = main_font.render(my_text, True, white)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)
pygame.display.flip()

stime = time.time()
state_time = time.time()
latest_left = "stop"
latest_right = "stop"
current_state = 0
pass_time = 0
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
	elif event.type == MOUSEBUTTONDOWN:
	    pos = pygame.mouse.get_pos()
            if quit.rect.collidepoint(pos):
                running = False
            if start.rect.collidepoint(pos):
                is_start = True
            if circle_rect.collidepoint(pos):
                re_draw = True
                if is_stop == False:
                    servo_motion(0,"stop")
                    servo_motion(1,"stop")
                    pass_time = time.time() -state_time
                else:
                    servo_motion(0,latest_left)
                    servo_motion(1,latest_right)
                is_stop = ~is_stop
        elif event.type == QUIT:
            running = False
    time.sleep(0.02)

    if is_stop:
        state_time = time.time()

    if is_start and time.time() - state_time > 3 - pass_time:
        state_time = time.time()
        state_change(current_state)
        current_state = (current_state + 1) % 7
        pass_time = 0

    if re_draw:
        screen.fill(black)
        if is_stop:
            circle_rect = pygame.draw.circle(screen, green, [160, 120], 35)
            screen.blit(resume.text_surface,resume.rect)
        else:
            circle_rect = pygame.draw.circle(screen, red, [160, 120], 35)
            screen.blit(stop.text_surface,stop.rect)
        screen.blit(start.text_surface,start.rect)
        screen.blit(quit.text_surface,quit.rect)
        screen.blit(left_history.text_surface,left_history.rect)
        screen.blit(right_history.text_surface,right_history.rect)
        for text_pos, my_text in left_history_info.items():
            text_surface = main_font.render(my_text, True, white)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
        for text_pos, my_text in right_history_info.items():
            text_surface = main_font.render(my_text, True, white)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
        pygame.display.flip()
        pygame.time.delay(15)
        re_draw = False

GPIO.cleanup()



