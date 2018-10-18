#! /bin/bash
#========================================================
#  Name: Test_fifo.py
#  Date: 2018-09-09
#  Author: Peng Wu(pw444) Junyi Shen(js3439)
#  Lab Number: One
#  Description: This bash script is used to start
#  python script on the background and start mplayer
#========================================================

#initialize the value for relevant variables
file_path=''
dir_path=''
play_file=''
script_path='/home/pi/Documents/Video_control.py'
temp_fifo='TempFIFO'
temp_dir='/home/pi/Documents'

#Analyze the argument, which will be passed to python script
while getopts "f:d:p:" arg
do
	case $arg in
	f)
		file_path="$OPTARG"
		echo $file_path
		;;
	d)
		dir_path="$OPTARG"
		echo $dir_path
		;;
	p)
		play_file="$OPTARG"
		echo $play_file
		;;
	?)
		echo "unknown argument"
		exit 1
		;;
	esac
done
#report error when no assigned play files
if [ -z "$play_file" ];then
	echo "unknown playing file"
	exit 1
fi
#auto generated a tempfifo if no assignment and run the python script on the background
if [ -n "$file_path" ];then
	${script_path} -f ${file_path} & 
elif [ -n "$dir_path" ];then
	mkfifo $dir_path/$temp_fifo
	file_path=$dir_path/$temp_fifo
	${script_path} -f ${file_path} &
else
	mkfifo $temp_dir/$temp_fifo
	file_path=$temp_dir/$temp_fifo
	${script_path} -f ${file_path} & 
fi
#start the mplayer to play the movie on PiTFT
sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -slave -quiet -input file=${file_path} -vo sdl -framedrop ${play_file}

