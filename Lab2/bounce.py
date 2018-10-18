#! /usr/bin/python
#========================================================
#  Name: bounce.py
#  Date: 2018-09-20
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: Two
#  Description: This python script is to display
#  one bouncing ball
#========================================================
import sys
import getopt as opt
import pygame
from pygame.locals import *
import os

# defind ball class
# arrtibutions: speed, image, rect and screen size
# function move: move accoring to the speed and bounce
# when touching screen
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

# switch the mode of display
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

#initial pygame
pygame.init()
pygame.mouse.set_visible(False)
size = width,height = 320,240
speed = [1,1]
black = 0,0,0
screen = pygame.display.set_mode(size)
#load ball image
ball_image = pygame.image.load("magic_ball_3.png")
ball= MagicBall(ball_image,speed,size)
running = True
#loop for updating ball position
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    ball.move()
    screen.fill(black)
    screen.blit(ball.image,ball.pos)
    pygame.display.flip()
    pygame.time.delay(15)
	

