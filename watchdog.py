#!/usr/bin/python
import sys
import subprocess
import os
import psutil

command = 'sudo /home/pi/checkdata.py > /dev/null &'
count = 0

for pid in psutil.pids():
	p = psutil.Process(pid)
	if p.name() == "checkdata.py":
		print("Checkdata running.  Called by " + str(p.cmdline()) )
		count = count + 1

if ( count == 0 ):   # not running
	print("Starting checkdata.py")
	g3 = subprocess.Popen('sudo /home/pi/checkdata.py > /dev/null &', shell=True, cwd="/run/shm", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	print("Waiting...")
	g3.wait
	print("Finished waiting!")
