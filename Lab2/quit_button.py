#! /usr/bin/python
#========================================================
#  Name: quit_button.py
#  Date: 2018-09-27
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: Two
#  Description: This python script is to display
#  quit button
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
#render quit button
quit = My_font('quit',white,(160,200))
screen.blit(quit.text_surface,quit.rect)
pygame.display.flip()
#loop for touch detection
running = True
while running:
    if not GPIO.input(quit_chan):
        break
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
	elif event.type == MOUSEBUTTONDOWN:
	    pos = pygame.mouse.get_pos()
   	elif event.type == MOUSEBUTTONUP:
	    pos = pygame.mouse.get_pos()
            if quit.rect.collidepoint(pos):
                running = False
        elif event.type == QUIT:
            running = False

GPIO.cleanup()

