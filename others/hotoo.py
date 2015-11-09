##################################################################
#hotobox main program
#author: moon & kyu
#

import RPi.GPIO as GPIO
import RPi.GPIO as io
import time
import os
import sys
import gspread
import datetime
import Adafruit_DHT
import signal
import json

GPIO.setmode(GPIO.BCM)

#####JSON FILE UPLOAD FUNCTION
def LOAD_JSON():
	in_file = open("sensorVar.json", "r")
	in_data = json.load(in_file)
	in_file.close()

def WRITE_JSON():
	out_file = open("sensorVar.json", "wb")
	json.dump(JSON_OBJ, out_file, indent=4)
	out_file.close()
		
JSON_OBJ=0

####### TEMP setup #######
TEMP_BUTTON_PIN=23
TEMP_BLUE_PIN=14
TEMP_GREEN_PIN=15

GPIO.setup(TEMP_BUTTON_PIN, GPIO.IN)		# button for TEMP
GPIO.setup(TEMP_BLUE_PIN, GPIO.OUT)			# LED for TEMP
GPIO.setup(TEMP_GREEN_PIN, GPIO.OUT)


# TEMP fuction
def RUN_TEMP():
	print "TEMP ON!"
	execfile("TEMP.py")

TEMP_ON=0
TEMP_PID=0
TEMP_FROM_WEB=1

# Signal handler
def TEMP_SIG(signal, frame):
	global TEMP_FROM_WEB
	TEMP_FROM_WEB=0

####### HUMID setup #######
HUMID_BUTTON_PIN=24
HUMID_BLUE_PIN=9
HUMID_GREEN_PIN=10

GPIO.setup(HUMID_BUTTON_PIN, GPIO.IN)        # button for HUMID
GPIO.setup(HUMID_BLUE_PIN, GPIO.OUT)			# LED for TEMP
GPIO.setup(HUMID_GREEN_PIN, GPIO.OUT)

# HUMID fuction
def RUN_HUMID():
	print "HMID ON!"
	execfile("HUMID.py")

HUMID_ON=0
HUMID_PID=0
HUMID_FROM_WEB=1

# Signal Handler
def HUMID_SIG(signal, frame):
	global HUMID_FROM_WEB
	HUMID_FROM_WEB=0

####### PIR setup #######
PIR_BUTTON_PIN=22
#PIR_LED_PIN=22

#GPIO.setup(PIR_LED_PIN, GPIO.OUT)	# LED for PIR
GPIO.setup(PIR_BUTTON_PIN, GPIO.IN)		# button for PIR

#PIR function
def RUN_PIR():
	print "Motion sensor on!"
	execfile("newPIR.py")

PIR_ON=0
PIR_PID=0
PIR_FROM_WEB=1

# Signal Handler
def PIR_SIG(signal, frame):
	global PIR_FROM_WEB
	PIR_FROM_WEB=0


####### DUST setup #######

DUST_BUTTON_PIN=25
DUST_BLUE_PIN=11
DUST_GREEN_PIN=8

GPIO.setup(DUST_BUTTON_PIN, GPIO.IN)	# button for DUST
GPIO.setup(DUST_BLUE_PIN, GPIO.OUT)	# LED for DUST
GPIO.setup(DUST_GREEN_PIN, GPIO.OUT)

def RUN_DUST():
	execfile("DUST.py")

DUST_ON=0
DUST_PID=0
DUST_FROM_WEB=1

# Signal handler
def DUST_SIG(signal, frame):
	global DUST_FROM_WEB
	DUST_FROM_WEB=0
	
# Parent's process ID
PARENT_PID = os.getpid()

os.system("sh replace.sh %d" % PARENT_PID)

print "press button"

try:

	while True:
		print ("loop...")

		# Calling signal handlers for interrupts from node.js
		signal.signal(signal.SIGBUS, TEMP_SIG)		# Temperature
		signal.signal(signal.SIGQUIT, HUMID_SIG)	# Humidity
		signal.signal(signal.SIGHUP, PIR_SIG)		# Motion
		signal.signal(signal.SIGILL, DUST_SIG)		# Dust

		
		# TEMP control
		if GPIO.input(TEMP_BUTTON_PIN)==0 or TEMP_FROM_WEB == 0:
		
			TEMP_ON+=1

			TEMP_FROM_WEB=1
			print "TEMP button pressed!"

			if (TEMP_ON % 2) == 1:
		#		GPIO.output(TEMP_LED_PIN, True)
			
				TEMP_PID = os.fork()	

				if TEMP_PID == 0:
					RUN_TEMP()			
		
				pids=(os.getpid(), TEMP_PID)

				print "parent pid: %d, child: %d" % pids
				
				time.sleep(0.5)

			else:
				print "TEMP OFF"
#				GPIO.output(TEMP_LED_PIN, False)
				os.system("sudo kill -s SIGTERM %d" % TEMP_PID)  #kill child process
				print "killed child process %d" % TEMP_PID	
				time.sleep(0.5)
		
		#HUMID control
		if GPIO.input(HUMID_BUTTON_PIN)==0 or HUMID_FROM_WEB==0:
			HUMID_ON+=1

			HUMID_FROM_WEB=1

			print "HUMID button pressed!"

			if (HUMID_ON % 2) == 1:
		#		GPIO.output(HUMID_LED_PIN, True)

				HUMID_PID = os.fork()

				if HUMID_PID == 0:
					RUN_HUMID()

				pids=(os.getpid(), HUMID_PID)

				print "parent pid: %d, child: %d" % pids

				time.sleep(0.5)
		
			else:
				print "HUMID OFF!"
#				GPIO.output(HUMID_LED_PIN, False)
				os.system("sudo kill -s SIGTERM %d" % HUMID_PID) #kill child process
				print "killed child process %d" % HUMID_PID
				time.sleep(0.5)

		# PIR control
		if GPIO.input(PIR_BUTTON_PIN)==0 or PIR_FROM_WEB==0:
			PIR_ON+=1

			PIR_FROM_WEB=1

			print "PIR button pressed!"

			if (PIR_ON % 2) == 1:
				print "Odd!!!"

#				GPIO.output(PIR_LED_PIN, True)
			
				PIR_PID = os.fork()	

				if PIR_PID == 0:
					RUN_PIR()			
		
				pids=(os.getpid(), PIR_PID)

				print "parent pid: %d, child: %d" % pids
				
				time.sleep(0.5)

			else:
				print "Even!!!"
#				GPIO.output(PIR_LED_PIN, False)
				os.system("sudo kill -s SIGTERM %d" % PIR_PID)  #kill child process
				print "killed child process %d" % PIR_PID	
				time.sleep(0.5)
	
		# DUST control
		if GPIO.input(DUST_BUTTON_PIN)==0 or DUST_FROM_WEB==0:
			DUST_ON+=1

			DUST_FROM_WEB=1

			print "DUST button pressed!"

			if (DUST_ON % 2) == 1:
				print "Odd!!!"

				#GPIO.output(23, True)
		
				DUST_PID = os.fork()	
				if DUST_PID == 0:
					RUN_DUST()			
		
				pids=(os.getpid(), DUST_PID)

				print "parent pid: %d, child: %d" % pids
				
				time.sleep(0.5)

			else:
				print "Even!!!"
		#		GPIO.output(23, False)
				os.system("sudo kill -s SIGTERM %d" % DUST_PID)  #kill child process
				print "killed child process %d" % DUST_PID	
				GPIO.output(17, GPIO.HIGH)			# manually turn the air cleaner off
				time.sleep(0.5)
	
		time.sleep(0.5)

except KeyboardInterrupt:
	GPIO.cleanup()
