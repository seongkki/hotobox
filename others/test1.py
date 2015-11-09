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

# Load sensorVar.json in 'in_data'
def LOAD_JSON():
        in_file = open("sensorVar.json", "r")
        global in_data
	in_data = json.load(in_file)
        in_file.close()
# Write on sensorVar.json with 'in_data'
def WRITE_JSON():
        out_file = open("sensorVar.json", "wb")
	json.dump(in_data, out_file, indent=4)
        out_file.close()

# Initialize all the values on sensorVar.json as zero
def INIT_JSON():
	in_data["sensorVar"]["humidVar"]=0
	in_data["sensorVar"]["tempVar"]=0
	in_data["sensorVar"]["pirVar"]=0
	in_data["sensorVar"]["dustVar"]=0
	in_data["pids"]["tempPID"]=0
	in_data["pids"]["humidPID"]=0
	in_data["pids"]["dustPID"]=0
	in_data["pids"]["pirPID"]=0
	in_data["ddong"]["Relay21"]=0
	WRITE_JSON()

# Update the status and interrupt values on JSON
def UPDATE_JSON(string, status):
	# interrupt 0: ready to get signal from button and web
	# status 0: relay only, 1: sensing + relay, 2: auto-mode 
	in_data["interrupts"]["%s"%string]=0
	in_data["status"]["%s"%string]=status
	WRITE_JSON()

####### TEMP setup #######
# TEMP pins
TEMP_BUTTON_PIN=23
TEMP_BLUE_PIN=14
TEMP_GREEN_PIN=15
TEMP_REL_PIN=18

# TEMP PIDs
TEMP_REL_PID=0
TEMP_PID=0
TEMP_SEN_PID=0

#TEMP attributes
TEMP_FROM_WEB=1
TEMP_AUTO_ON=0
TEMP_ON=0
TEMP_FIRST=1	# Is it the first iteration? Y: 1 / N: 0

### GPIO setup for TEMP ###
GPIO.setup(TEMP_BUTTON_PIN, GPIO.IN)		# button for TEMP
GPIO.setup(TEMP_BLUE_PIN, GPIO.OUT)             # LED for TEMP
GPIO.setup(TEMP_GREEN_PIN, GPIO.OUT)

### TEMP fuction
# Run on automode
def RUN_TEMP():
		print "TEMP AUTU-MODE ON!"
		execfile("TEMP.py")

# Run on sensing-only mode
def RUN_TEMP_SEN():
		print "TEMP SENSING-ONLY MODE ON!"
		execfile("TEMP_SEN.py")

# Run on relay mode
def RUN_TEMP_REL():
		print "TEMP RELAY ONLY MODE ON"
		execfile("TEMP_REL.py")
		if TEMP_AUTO_ON==1:
			TEMP_FROM_WEB=0

# Signal handler
#def TEMP_SIG(signal, frame):
#		global TEMP_FROM_WEB
#		TEMP_FROM_WEB=0

# Run relay mode as a default
#TEMP_REL_PID=os.fork()

#if TEMP_REL_PID==0:
#		TEMP_REL()

####### HUMID setup #######

#HUMID pins
HUMID_BUTTON_PIN=24
HUMID_BLUE_PIN=9
HUMID_GREEN_PIN=10


HUMID_ON=0
HUMID_PID=0
HUMID_FROM_WEB=1


GPIO.setup(HUMID_BUTTON_PIN, GPIO.IN)        # button for HUMID
GPIO.setup(HUMID_BLUE_PIN, GPIO.OUT)                    # LED for TEMP
GPIO.setup(HUMID_GREEN_PIN, GPIO.OUT)

# HUMID fuction
def RUN_HUMID():
	print "HUMID ON!"
	execfile("HUMID.py")

#HUMID AUTO MODE
def RUN_HUMID():
		print "HUMID AUTO ON"
		execfile("HUMID.py")

#HUMID SENSING ONLY MODE
def RUN_HUMID_SEN():
		print "HUMID SENSOR ON"
		execfile("HUMID_SEN.py")

#HUMID RELAY MODE
def RUN_HUMID_REL():
		print "HUMID RELAY MODE ON"
		execfile("HUMID_REL.py")
		if HUMID_AUTO_ON==1:
			HUMID_FROM_WEB=0

# Signal Handler
#def HUMID_SIG(signal, frame):
#	global HUMID_FROM_WEB
#	HUMID_FROM_WEB=0

####### PIR setup #######
#PIR_BUTTON_PIN=4
#PIR_LED_PIN=24

#GPIO.setup(PIR_LED_PIN, GPIO.OUT)	# LED for PIR
#GPIO.setup(PIR_BUTTON_PIN, GPIO.IN)		# button for PIR

#PIR function
#def RUN_PIR():
#	print "Motion sensor on!"
#	execfile("newPIR.py")

#PIR_ON=0
#PIR_PID=0
#PIR_FROM_WEB=1

# Signal Handler
#def PIR_SIG(signal, frame):
#	global PIR_FROM_WEB
#	PIR_FROM_WEB=0


####### DUST setup #######


DUST_BUTTON_PIN=25
DUST_BLUE_PIN=11
DUST_GREEN_PIN=8

GPIO.setup(DUST_BUTTON_PIN, GPIO.IN)    # button for DUST
GPIO.setup(DUST_BLUE_PIN, GPIO.OUT)     # LED for DUST
GPIO.setup(DUST_GREEN_PIN, GPIO.OUT)

def RUN_DUST():
	execfile("DUST.py")

DUST_ON=0
DUST_PID=0
DUST_FROM_WEB=1

#HUMID AUTO MODE
def RUN_DUST():
		print "DUST AUTO ON"
		execfile("DUST.py")

#HUMID SENSING ONLY MODE
def RUN_DUST_SEN():
		print "DUST SENSOR ON"
		execfile("DUST_SEN.py")

#HUMID RELAY MODE
def DUST_REL():
		print "DUST RELAY MODE ON"
		execfile("DUST_REL.py")
		if DUST_AUTO_ON==1:
			HUMID_FROM_WEB=0

# Signal handler
#def DUST_SIG(signal, frame):
#	global DUST_FROM_WEB
#	DUST_FROM_WEB=0

# Load json 
LOAD_JSON()

# Initialize json
INIT_JSON()

# Put parent's process ID onto sensorVar.json
PARENT_PID = os.getpid()

print "Parent PID: %d"%PARENT_PID

in_data["pids"]["parent"] = PARENT_PID

WRITE_JSON()


print "press button"

try:

	while True:
		print ("loop...")

		# Calling signal handlers for interrupts from node.js
#		signal.signal(signal.SIGBUS, TEMP_SIG)		# Temperature
#		signal.signal(signal.SIGQUIT, HUMID_SIG)	# Humidity
#		signal.signal(signal.SIGHIP, PIR_SIG)		# Motion
#		signal.signal(signal.SIGILL, DUST_SIG)		# Dust

		# TEMP control
		if GPIO.input(TEMP_BUTTON_PIN)==0 or in_data["interrupts"]["temp"] == 1:
		
			TEMP_ON+=1
		
			print "TEMP button pressed!"

			if (TEMP_ON % 3) == 1:
				print "sensing mode"

				UPDATE_JSON("temp", 1)

				if TEMP_FIRST == 1:			 # if it is the first time run this node
					TEMP_REL_PID=os.fork()
					
					if TEMP_REL_PID == 0:
						RUN_TEMP_REL()
					
					TEMP_FIRST=0
					
				GPIO.output(TEMP_BLUE_PIN, True) #blue LED on
			
				TEMP_SEN_PID=os.fork()
				if TEMP_SEN_PID==0:
					RUN_TEMP_SEN()
				

				time.sleep(0.5)
		
			elif (TEMP_ON % 3) == 2:

				print "Auto mode ON!"

				UPDATE_JSON("temp", 2)
			
				TEMP_AUTO_ON=1

				#Green LED on
				GPIO.output(TEMP_BLUE_PIN, 0)		 #blue LED off
				GPIO.output(TEMP_GREEN_PIN, True)	 #green LED on
				
				os.system("sudo kill -s SIGTERM %d" % TEMP_REL_PID)
				os.system("sudo kill -s SIGTERM %d" % TEMP_SEN_PID)
				
				TEMP_PID = os.fork()	

				if TEMP_PID == 0:
					RUN_TEMP()			
	
				pids=(os.getpid(), TEMP_PID)

				print "parent pid: %d, child: %d" % pids
				
				time.sleep(0.5)

			else:
				# LED off
				GPIO.output(TEMP_GREEN_PIN, 0) #green LED on
					
				print "TEMP RELAY MODE"
				
				UPDATE_JSON("temp", 0)
				
				TEMP_AUTO_ON=0

				os.system("sudo kill -s SIGTERM %d" % TEMP_PID)  #kill child process
				
				print "killed AUTO MODE %d" % TEMP_PID	

				TEMP_REL_PID=os.fork()

				if TEMP_REL_PID==0:
					RUN_TEMP_REL()

				time.sleep(0.5)
		
		#HUMID control
		if GPIO.input(HUMID_BUTTON_PIN)==0 or HUMID_FROM_WEB==0:
			HUMID_ON+=1

			HUMID_FROM_WEB=1

			print "HUMID button pressed!"

			if (HUMID_ON % 3) == 1:
			
				print "Humid sensing mode!"

				GPIO.output(HUMID_BLUE_PIN, True) #Blue LED

				HUMID_SEN_PID = os.fork()

				if HUMID_SEN_PID == 0:
					RUN_SEN_HUMID()

				time.sleep(0.5)

			elif (HUMID_ON % 3) == 2:

				#Green LED on
				GPIO.output(HUMID_BLUE_PIN, 0) #Blue LED off
				GPIO.output(HUMID_GREEN_PIN, True) #Green LED on

				print "HUMID Automode on!"
				
				HUMID_AUTO_ON = 1

				os.system("sudo kill -s SIGTERM %d" % HUMID_SEN_PID)

				HUMID_PID = os.fork()

				if HUMID_PID == 0:
					RUN_HUMID()
					
				pids=(os.getpid(), HUMID_PID)

				print "parent pid: %d, child: %d" % pids

				time.sleep(0.5)
		
			else:
				# LED off
				GPIO.output(HUMID_GREEN_PIN, 0) #Green LED off
				
				print "HUMID OFF!"
				
				HUMID_AUTO_ON = 0

				os.system("sudo kill -s SIGTERM %d" % HUMID_PID)

				print "killed child process %d" % HUMID_PID

				time.sleep(0.5)

		# PIR control
#		if GPIO.input(PIR_BUTTON_PIN)==0 or PIR_FROM_WEB==0:
#			PIR_ON+=1

#			PIR_FROM_WEB=1

#			print "PIR button pressed!"

#			if (PIR_ON % 2) == 1:
#				print "Odd!!!"

#				GPIO.output(PIR_LED_PIN, True)
			
#				PIR_PID = os.fork()	

#				if PIR_PID == 0:
#					RUN_PIR()			
		
#				pids=(os.getpid(), PIR_PID)

#				print "parent pid: %d, child: %d" % pids
				
#				time.sleep(0.5)

#			else:
#				print "Even!!!"
#				GPIO.output(PIR_LED_PIN, False)
#				os.system("sudo kill -s SIGTERM %d" % PIR_PID)  #kill child process
#				print "killed child process %d" % PIR_PID	
#				time.sleep(0.5)
	
		# DUST control
#		if GPIO.input(21)==0 or DUST_FROM_WEB==0:
#			DUST_ON+=1

#			DUST_FROM_WEB=1

#			print "DUST button pressed!"

#			if (DUST_ON % 2) == 1:
#				print "Odd!!!"

#				GPIO.output(23, True)
			
#				DUST_PID = os.fork()	

#				if DUST_PID == 0:
#					RUN_DUST()			
		
#				pids=(os.getpid(), DUST_PID)

#				print "parent pid: %d, child: %d" % pids
				
#				time.sleep(0.5)

#			else:
#				print "Even!!!"
#				GPIO.output(23, False)
#				os.system("sudo kill %d" % DUST_PID)  #kill child process
#				print "killed child process %d" % PIR_PID	
#				os.system("sudo kill %d" % DUST_PID)  #kill child process
#				time.sleep(0.5)
	
		time.sleep(0.5)

except KeyboardInterrupt:
	GPIO.cleanup()
