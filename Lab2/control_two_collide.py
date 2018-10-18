#! /usr/bin/python
#========================================================
#  Name: control_two_Collide.py
#  Date: 2018-09-27
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: Two
#  Description: This python script is to display
#  two menus and control for animation
#========================================================
import sys
import getopt as opt
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO
import os

#class for font button
class My_font:
    def __init__(self, text, color, pos, size = 40):
        self.font = pygame.font.Font(None, size)
	self.text_surface = self.font.render(text,True,color)
        self.rect = self.text_surface.get_rect(center = pos)
# defind ball class
# arrtibutions: speed, image, rect and screen size
# function move: move accoring to the speed and bounce
# when touching screen
# function collide: update speed when collision occurs
class MagicBall:
    def __init__(self, image, speed, screen):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect()
        self.screen = screen
    def move(self):
        self.pos = self.pos.move(self.speed)
        if self.pos.left < 0 or self.pos.right > self.screen[0]:
    	    self.speed[0] = -self.speed[0]
        if self.pos.top < 0 or self.pos.bottom > self.screen[1]:
    	    self.speed[1] = -self.speed[1]
    def collide(self, ball):
        if self.pos.colliderect(ball.pos):
            deltax = self.pos.centerx - ball.pos.centerx
            deltay = self.pos.centery - ball.pos.centery
            deltavx = self.speed[0] - ball.speed[0]
            deltavy = self.speed[1] - ball.speed[1]
            distance = deltax * deltax + deltay * deltay
            temp = deltax * deltavx + deltay * deltavy
            change_vx = -deltax * temp / distance
            change_vy = -deltay * temp / distance
            self.speed[0] = self.speed[0] + change_vx
            self.speed[1] = self.speed[1] + change_vy
            ball.speed[0] = ball.speed[0] - change_vx
            ball.speed[1] = ball.speed[1] - change_vy

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
#set up bail out button
GPIO.setmode(GPIO.BCM)
quit_chan = 27
GPIO.setup(quit_chan,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#initialize pygame
pygame.init()
if display_on_piTFT:
    pygame.mouse.set_visible(False)
else:
    pygame.mouse.set_visible(True)
size = width,height = 320,240
black = 0,0,0
white = 255,255,255
screen = pygame.display.set_mode(size)
screen.fill(black)

#prepare all the button
quit = My_font('quit',white,(220,210))
start = My_font('start',white,(100,210))
pause = My_font('Pause',white,(70,210),25)
restart = My_font('Restart',white,(70,210),25)
fast = My_font('Fast',white,(130,210),25)
slow = My_font('Slow',white,(190,210),25)
back = My_font('Back',white,(250,210),25)
screen.blit(quit.text_surface,quit.rect)
screen.blit(start.text_surface,start.rect)
#prepare ball images
smaller_size = 320,200
speed1 = [1,1]
speed2 = [2,2]
ball_image_1 = pygame.image.load("magic_ball_3.png")
ball_image_2 = pygame.image.load("magic_ball_3.png")
ball_1 = MagicBall(ball_image_1,speed1,smaller_size)
ball_2 = MagicBall(ball_image_2,speed2,smaller_size)
ball_1.pos.move_ip(10,20)
ball_2.pos.move_ip(60,120)

pygame.display.flip()
#initialize control signals
running = True
run_two_ball = False
show_coordinate = False
is_Pause = False
#initialize collision detection delay, coordination
#present period, maximum and minimum display speed
#and step
max_count = 2
count = 0
display_count = 0
max_display_count = 3
sleep_time = 20
max_sleep_time = 35
min_sleep_time = 5
step = 7

while running:
    if not GPIO.input(quit_chan):
        break
    if display_count > 0:
        display_count -= 1
    if show_coordinate and display_count == 0:
        show_coordinate = False
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
	elif event.type == MOUSEBUTTONDOWN:
	    pos = pygame.mouse.get_pos()
            if not run_two_ball:
                if quit.rect.collidepoint(pos):
                    running = False
                    break
                elif start.rect.collidepoint(pos):
                    run_two_ball = True
                else:
                    show_coordinate = True
                    display_count = max_display_count
            else:
                #check whether to pause
                if pause.rect.collidepoint(pos):
                    is_Pause = ~is_Pause
                #check the display speed
                elif slow.rect.collidepoint(pos):
                    sleep_time = min(max_sleep_time,sleep_time+step)
                elif fast.rect.collidepoint(pos):
                    sleep_time = max(min_sleep_time,sleep_time-step)
                elif back.rect.collidepoint(pos):
                    run_two_ball = False
                else:
                    show_coordinate = True
                    display_count = max_display_count
        elif event.type == QUIT:
            running = False
    
    screen.fill(black)
    #check whether to show coordination
    if show_coordinate:
        coordinate = My_font('touch at ' + str(pos), white,(160,80))
        screen.blit(coordinate.text_surface,coordinate.rect)
    #check whether to show balls
    if run_two_ball:
        if not is_Pause:
            if count > 0:
	        count -= 1
            elif count == 0:
                if ball_1.pos.colliderect(ball_2.pos):
                    ball_1.collide(ball_2)
                    count = max_count
            ball_1.move()
            ball_2.move()
            screen.blit(pause.text_surface,pause.rect)
        else:
            screen.blit(restart.text_surface,restart.rect)

        screen.blit(ball_1.image,ball_1.pos)
        screen.blit(ball_2.image,ball_2.pos)
        screen.blit(fast.text_surface,fast.rect)
        screen.blit(slow.text_surface,slow.rect)
        screen.blit(back.text_surface,back.rect)
    else:
        screen.blit(quit.text_surface,quit.rect)
        screen.blit(start.text_surface,start.rect)
    pygame.display.flip()
    pygame.time.delay(sleep_time)

GPIO.cleanup()

	

