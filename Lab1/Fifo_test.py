#! /usr/bin/python
#========================================================
#  Name: Test_fifo.py
#  Date: 2018-09-09
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: One
#  Description: This python script is used to control
#  mplayer by fifo file
#========================================================
import sys 
import getopt as opt
import os 
import stat
import random
import thread
import time

#=================================================
# Function of printing help Manual for beginners
#=================================================
def helpManual():
    print '========================================'
    print 'Usage Help: ./fifo_test.py -{h|D|f|d} <options> args'
    print '-h, --help: show the help manual'
    print '-f, --file[file_path]: assign the path for fifo file'
    print '-d, --directory[dir_path]: assign the dir_path for fifo file creation'
    print '-D, --Debug: turn on the Debug mode for more print information'
    print '========================================'

#=================================================
# Function of analyzing arguments
#=================================================
def argAnalysis():
    dict = {'file':'','directory':'','Debug':'False','playFile':[]}
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
        dict['playFile'] = args
        return dict
    except opt.GetoptError:
        print 'The error occurs in arguments'
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

#======================================================
# Function of starting mplayer 
#======================================================
def startMplayer(file_path, playfile):
    os.system('sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -vo sdl -slave -quiet -input file=' + file_path + ' ' + playfile)
    
    
if "__main__" == __name__:
    #Analysize and obtain the arguments
    dict = argAnalysis()
    #Check the validity of arguments
    if len(dict['playFile']) == 0:
        print "the error occurs in empty file"
        helpManual()
        exit(1)
    file_path = dict['file']
    dir_path = dict['directory'] 
    if dict['Debug'] == 'True':
        print dict
    file_path = fifoCreation(file_path,dir_path)
    print file_path
    #open a new thread for mplayer
    thread.start_new_thread(startMplayer,(file_path,''.join(dict['playFile'])))
    time.sleep(2)
    #loop for waiting the input command
    while True:
        command = raw_input('Please input your command:\n')
        command_ext = 'echo ' + command + ' > ' + file_path
        if(dict['Debug'] == 'True'):
            print command_ext
        os.system(command_ext)
        if(command == 'quit'):
            break

    if file_path != dict['file']:
        os.system('rm ' + file_path)


    
