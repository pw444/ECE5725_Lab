#! /usr/bin/python
#========================================================
#  Name: two_collide.py
#  Date: 2018-09-20
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: Two
#  Description: This python script is to display
#  two bouncing ball and handle collision with each other
#========================================================
import pygame
import sys
from pygame.locals import *
import os
import getopt as opt

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
speed1 = [1,1]
speed2 = [2,2]
black = 0,0,0
screen = pygame.display.set_mode(size)
#load ball image and move to different initial position
ball_image_1 = pygame.image.load("magic_ball_3.png")
ball_image_2 = pygame.image.load("magic_ball_3.png")
ball_1 = MagicBall(ball_image_1,speed1,size)
ball_2 = MagicBall(ball_image_2,speed2,size)
ball_1.pos.move_ip(10,20)
ball_2.pos.move_ip(60,80)
running = True

#define for collision detection delay
max_count = 2
count = 0

#loop for updating ball position
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    if count > 0:
	 count -= 1
    elif count == 0:
        if ball_1.pos.colliderect(ball_2.pos):
            ball_1.collide(ball_2)
            count = max_count
    ball_1.move()
    ball_2.move()
    screen.fill(black)
    screen.blit(ball_1.image,ball_1.pos)
    screen.blit(ball_2.image,ball_2.pos)
    pygame.display.flip()
    pygame.time.delay(15)
	

