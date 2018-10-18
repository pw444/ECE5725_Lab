#! /usr/bin/python
#========================================================
#  Name: More_video_control_cb.py
#  Date: 2018-09-20
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: Two
#  Description: This python script is used to control
#  mplayer by buttons on PiTFT and two external buttons 
#  by callback functions
#========================================================
import sys 
import getopt as opt
import os 
import stat
import random
import RPi.GPIO as GPIO
import time

#=================================================
# Function of printing help Manual for beginners
#=================================================
def helpManual():
    print '========================================'
    print 'Usage Help: ./fifo_test.py -{h|D|f|d} <options> args'
    print '-h, --help: show the help manual'
    print '-f, --file + file_path: assign the path for fifo file'
    print '-d, --directory + dir_path: assign the dir_path for fifo file creation'
    print '-D, --Debug: turn on the Debug mode for more print information'
    print '========================================'

#=================================================
# Function of analyzing arguments
#=================================================
def argAnalysis():
    dict = {'file':'','directory':'','Debug':'False'}
    try:
        opts, args = opt.getopt(sys.argv[1:], "hDf:d:", ["help", "Debug", "file=", "directory="])  
        for o,a in opts:
            if o in ("-h", "--help"):
                helpManual()
                exit(0)
            elif o in ("-f", "--file"):
                dict['file'] = a
            elif o in ("-d", "--directory"):
                dict['directory'] = a
            elif o in ("-D", "--Debug"):
                dict['Debug'] = 'True'
        return dict
    except opt.GetoptError:
        print 'Argument error occurs'
        helpManual()
        exit(1)

#==================================================
# Function of creating a fifo file automatically or
# assigning the exist one
#==================================================
def fifoCreation(file_path,dir_path):
    # random four tail number generator to get rid of same fifo name
    randomTail = ''.join(str(random.choice(range(10))) for _ in range(4))
    # decision on creating a new one or assigning an existing one
    if file_path == '' and dir_path == '':
        file_path = os.getcwd() + '/tempFIFO' + randomTail
        os.system('mkfifo ' + file_path)
    elif file_path != '':
        if not os.path.exists(file_path):
            print 'file path does not exist'
            exit(1)
        mode = os.stat(file_path).st_mode
        if not stat.S_ISFIFO(mode):
            print 'the assigned file is not a FIFO file'
            choice = raw_input("Do you want to generate a temp FIFO file automatically?[y/n]")
            if choice.lower() in ('y','yes'):
                file_path = os.getcwd() + '/tempFIFO' + randomTail
                os.system('mkfifo ' + file_path)
            else:
                print 'The error occurs in file type'
                exit(1)
    else:
        if not os.path.isdir(dir_path):
            print 'the dir_path is wrong!'
            exit(1)
        file_path = dir_path + '/tempFIFO' + randomTail
        os.system('mkfifo ' + file_path)
    return file_path


if "__main__" == __name__:
    #Analysize and obtain the arguments
    dict = argAnalysis()
    #Check the validity of arguments
    file_path = dict['file']
    dir_path = dict['directory'] 
    if(dict['Debug'] == 'True'):
        print dict
    file_path = fifoCreation(file_path,dir_path)
    print file_path
    #initialize the GPIO pin number list, quit channel and mode for GPIO
    chan_list = [17,22,23,13,19]
    quit_chan = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(chan_list,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(quit_chan,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    time_interval = 0.3
    #define the funtions for each GPIO pin
    operation = {'17':'pause','22':'seek 10','23':'seek -10','27':'quit','13':'seek 30','19':'seek -30'}
    #defien the callback functions
    def GPIO_callback(channel):
        os.system('echo ' + operation[str(channel)] + ' > ' + file_path)
    #loop for binding the GPIO pins with callback functions
    for chan in chan_list:
        GPIO.add_event_detect(chan,GPIO.FALLING,callback=GPIO_callback,bouncetime=300)
    #waiting for the quit button pressed
    try:
        GPIO.wait_for_edge(quit_chan,GPIO.FALLING)
        os.system('echo ' + operation[str(quit_chan)] + ' > ' + file_path)
    except KeyboardInterrupt:
        GPIO.cleanup()
    #clean up the GPIO and remove the generated files
    GPIO.cleanup()
    os.system('rm ' + file_path)


    
