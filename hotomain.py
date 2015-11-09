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

os.system("sudo python clean.py")

web=os.fork()

if web==0:
	os.system("sudo node web.js")
	exit()




GPIO.setmode(GPIO.BCM)

############# JSON FILE UPLOAD FUNCTION ###############

# LOAD_JSON -> LOAD_COUNTER_JSON
# WRITE_JSON -> WRITE_COUNTER_JSON
# Create LOAD_INTER_JSON and WRITE_INTER_JSON

# Load sensorVar.json in 'in_data'
def LOAD_COUNTER_JSON():
        in_counter_file = open("counter.json", "r")
	global in_counter
	while True:
		try:
			in_counter = json.load(in_counter_file)
			break
		except:
			print "[COUNTER JSON] Loading error"
        in_counter_file.close()

# Write on sensorVar.json with 'in_data'
def WRITE_COUNTER_JSON():
        out_counter_file = open("counter.json", "wb")
	json.dump(in_counter, out_counter_file, indent=4)
        out_counter_file.close()

# Load sensorVar.json in 'in_data'
def LOAD_INTER_JSON():
        in_inter_file = open("inter.json", "r")
	global in_inter
	while True:
		try:
			in_inter = json.load(in_inter_file)
			break
		except:
			print "[INTER JSON] Loading error"
        in_inter_file.close()

# Write on sensorVar.json with 'in_data'
def WRITE_INTER_JSON():
        out_inter_file = open("inter.json", "wb")
	json.dump(in_inter, out_inter_file, indent=4)
        out_inter_file.close()

# Load sensorVar.json in 'in_data'
def LOAD_REL_JSON():
        in_rel_int_file = open("rel_int.json", "r")
	global in_rel_int
	while True:
		try:
			in_rel_int = json.load(in_rel_int_file)
			break
		except:
			print "[REL_INTER JSON] Loading error"
        
	in_rel_int_file.close()

	in_rel_on_file = open("rel_on.json", "r")
	global in_rel_on
	while True:
		try:
			in_rel_on = json.load(in_rel_on_file)
			break
		except:
			print "[REL_ON JSON] Loading error"

        in_rel_on_file.close()

# Write on sensorVar.json with 'in_data'
def WRITE_REL_JSON():
        out_rel_int_file = open("rel_int.json", "wb")
	json.dump(in_rel_int, out_rel_int_file, indent=4)
        out_rel_int_file.close()
        
	out_rel_on_file = open("rel_on.json", "wb")
	json.dump(in_rel_on, out_rel_on_file, indent=4)
        out_rel_on_file.close()

# Initialize all the values on sensorVar.json as zero
def INIT_JSON():
	### Initialize sensor counters
	in_counter["counter"]["humid"]=0
	in_counter["counter"]["temp"]=0
	in_counter["counter"]["pir"]=0
	in_counter["counter"]["dust"]=0
	###
	
	### Initialize parent process' PID
	in_counter["pids"]["parent"]=0
	###
	
	WRITE_COUNTER_JSON()
	
	### Initialize interrupt variables
	in_inter["interrupt"]["temp"]=0
	in_inter["interrupt"]["humid"]=0
	in_inter["interrupt"]["dust"]=0
	in_inter["interrupt"]["pir"]=0
	###

	WRITE_INTER_JSON()

def INIT_REL_JSON():
	### Initialize relay values
	in_rel_int["interrupt"]["temp"]=0
	in_rel_int["interrupt"]["humid"]=0
	in_rel_int["interrupt"]["dust"]=0
	in_rel_int["interrupt"]["extra"]=0
	###
	
	in_rel_on["ON"]["temp"]=0
	in_rel_on["ON"]["humid"]=0
	in_rel_on["ON"]["dust"]=0
	in_rel_on["ON"]["extra"]=0
	###

	WRITE_REL_JSON()

# Update the counter and interrupt values on JSON files
def UPDATE_JSON(sensor,counter):
	# interrupt 0: ready to get signal from button and web
	# status 0: relay only, 1: sensing + relay, 2: auto-mode 
	in_inter["interrupt"]["%s"%sensor]=0
	WRITE_INTER_JSON()
	in_counter["counter"]["%s"%sensor]=counter
	WRITE_COUNTER_JSON()

# Load a counter value from file.json
def LOAD_VAL(file, sensor):
	if in_inter == file:
		rv = file["interrupt"]["%s"%sensor]
	
	elif in_counter == file:
		rv = file["counter"]["%s"%sensor]
		
	return rv

# Store a value to json file
def WRITE_INTER_VAL(var, value):
	in_counter["interrupt"]["%s"%var] = value
	WRITE_COUNTER_JSON()
	
# Store a value to json file
def WRITE_COUNTER_VAL(var, value):
	in_inter["counter"]["%s"%var] = value
	WRITE_INTER_JSON()
	
################################# TEMP setup ###############################

### TEMP pins
TEMP_BUTTON_PIN=23
TEMP_BLUE_PIN=14
TEMP_GREEN_PIN=15
TEMP_REL_PIN=27
###

### TEMP PIDs
TEMP_REL_PID=0
TEMP_PID=0
TEMP_SEN_PID=0
###

###TEMP attributes
TEMP_AUTO_ON=0
TEMP_CNT=0
###

### GPIO setup for TEMP ###
GPIO.setup(TEMP_BUTTON_PIN, GPIO.IN)		# button for TEMP
GPIO.setup(TEMP_BLUE_PIN, GPIO.OUT)             # LED for TEMP
GPIO.setup(TEMP_GREEN_PIN, GPIO.OUT)

### TEMP fuction
# Run on automode
def RUN_TEMP():
		print "TEMP AUTU-MODE ON!"
		#execfile("TEMP.py")
		os.system("sudo python TEMP.py")
# Run on sensing-only mode
def RUN_TEMP_SEN():
		print "TEMP SENSING-ONLY MODE ON!"
		#execfile("TEMP_SEN.py")
		os.system("sudo python TEMP_SEN.py")
# Run on relay mode
def RUN_TEMP_REL():
		print "TEMP RELAY ONLY MODE ON"
		#execfile("TEMP_REL.py")
		os.system("sudo python TEMP_REL.py")
###

############################### HUMID setup ################################

### HUMID pins
HUMID_BUTTON_PIN=24
HUMID_BLUE_PIN=10
HUMID_GREEN_PIN=9
HUMID_REL_PIN=17
###

### HUMID PIDs
HUMID_REL_PID=0
HUMID_SEN_PID=0
HUMID_PID=0
###

### HUMID attributes
HUMID_CNT=0
###

### HUMID GPIO setup
GPIO.setup(HUMID_BUTTON_PIN, GPIO.IN)        # button for HUMID
GPIO.setup(HUMID_BLUE_PIN, GPIO.OUT)                    # LED for TEMP
GPIO.setup(HUMID_GREEN_PIN, GPIO.OUT)
###

### HUMID fuction

# HUMID AUTO MODE
def RUN_HUMID():
		print "HUMID AUTO ON"
		execfile("HUMID.py")

# HUMID SENSING ONLY MODE
def RUN_HUMID_SEN():
		print "HUMID SENSOR ON"
		execfile("HUMID_SEN.py")

# HUMID RELAY MODE
def RUN_HUMID_REL():
		print "HUMID RELAY MODE ON"
		execfile("HUMID_REL.py")


################################## DUST setup ###############################

### DUST pins
DUST_BUTTON_PIN=22
DUST_BLUE_PIN=11
DUST_GREEN_PIN=8
DUST_REL_PIN=18
###

### DUST PIDs
DUST_PID=0
DUST_REL_PID=0
DUST_SEN_PID=0
###

### DUST attributes
DUST_CNT=0
###

### DUST GPIO setup
GPIO.setup(DUST_BUTTON_PIN, GPIO.IN)    # button for DUST
GPIO.setup(DUST_BLUE_PIN, GPIO.OUT)     # LED for DUST
GPIO.setup(DUST_GREEN_PIN, GPIO.OUT)
###

### DUST functions 

#HUMID AUTO MODE
def RUN_DUST():
		print "DUST AUTO ON"
		execfile("DUST.py")

#HUMID SENSING ONLY MODE
def RUN_DUST_SEN():
		print "DUST SENSOR ON"
		execfile("DUST_SEN.py")

#HUMID RELAY MODE
def RUN_DUST_REL():
		print "DUST RELAY MODE ON"
		execfile("DUST_REL.py")
###

############################ PIR setup ################################

### PIR pins
PIR_BUTTON_PIN=25
PIR_LED_PIN=7
###

### PIR PIDs
PIR_PID=0
###

### PIR attributes
PIR_CNT=0
###

### PIR GPIO setup
GPIO.setup(PIR_LED_PIN, GPIO.OUT)		# LED for PIR
GPIO.setup(PIR_BUTTON_PIN, GPIO.IN)		# button for PIR
###

### PIR function
def RUN_PIR():
	print "Motion sensor on!"
	execfile("PIR.py")
###

########### EXTRA RELAY ############
# EXRTRA relay PID
EXTRA_PID=0

### EXTRA function
def RUN_EXTRA_REL():
	execfile("EXTRA_REL.py")
###

##########################################################
################ Pre-process for service #################
##########################################################

## Load json 
LOAD_INTER_JSON()
LOAD_COUNTER_JSON()
LOAD_REL_JSON()

## Initialize values in inter.json and counter.json
INIT_JSON()
INIT_REL_JSON()

## Put parent's process ID onto sensorVar.json
PARENT_PID = os.getpid()

print "Parent PID: %d"%PARENT_PID

#in_counter["pids"]["parent"] = PARENT_PID

#WRITE_COUNTER_JSON()

######### Activating all the relay control #########

### TEMP
TEMP_REL_PID=os.fork()
	
if TEMP_REL_PID == 0:
	RUN_TEMP_REL()
	exit()
###

### HUMID
HUMID_REL_PID=os.fork()
					
if HUMID_REL_PID == 0:
	RUN_HUMID_REL()
	exit()
###

### DUST
DUST_REL_PID=os.fork()
					
if DUST_REL_PID == 0:
	RUN_DUST_REL()
	exit()
###

###EXTRA 
EXTRA_REL_PID=os.fork()
					
if EXTRA_REL_PID == 0:
	RUN_EXTRA_REL()
	exit()
###	

################################################ Service Start ####################################################

print "HOTO BOX 2015"
print "Created by Kyu and Moon"

try:
	while True:
		print ("LISTENING...")
	

		LOAD_COUNTER_JSON()
		LOAD_INTER_JSON()

		### TEMP control
		if GPIO.input(TEMP_BUTTON_PIN)==0 or LOAD_VAL(in_inter, "temp") == 1:
	
			### Load temp counter and update on json 
			TEMP_CNT = LOAD_VAL(in_counter,"temp") + 1

			#WRITE_VAL_JSON("counter", "temp", TEMP_CNT)
			UPDATE_JSON("temp", TEMP_CNT)
			###

			print "TEMP button pressed!"

			if (TEMP_CNT % 3) == 1:
				print "Sensing + Relay Mode"
			
				### Blue LED on
				GPIO.output(TEMP_BLUE_PIN, True)
				###

				### Create a child process for sensing
				TEMP_SEN_PID=os.fork()
				if TEMP_SEN_PID==0:
					RUN_TEMP_SEN()
					print "bye"
					exit()
				###

				time.sleep(0.5)
		
			elif (TEMP_CNT % 3) == 2:


				LOAD_REL_JSON()
				if in_rel_on["ON"]["temp"]==1:
					in_rel_int["interrupt"]["temp"]=1
					WRITE_REL_JSON()
				
					while in_rel_on["ON"]["temp"]:
						LOAD_REL_JSON()
				
				print "Auto mode ON!"
				

				### Blue LED off / Green LED on
				GPIO.output(TEMP_BLUE_PIN, 0)		 #blue LED off
				GPIO.output(TEMP_GREEN_PIN, True)	 #green LED on
				###

				### stop Sensing and Relay control
				os.system("sudo kill -s SIGTERM %d" % TEMP_REL_PID)
				os.system("sudo kill -s SIGTERM %d" % TEMP_SEN_PID)
				###

				### Create a child process for AUTO mode
				TEMP_PID = os.fork()	
				
			#	os.waitpid(TEMP_SEN_PID,0)
			#	os.waitpid(TEMP_REL_PID,0)

				if TEMP_PID == 0:
					print "auto mode"
					RUN_TEMP()	
					print "bye"
					exit()
				###
				
				time.sleep(0.5)

			else:
				### Green LED off
				GPIO.output(TEMP_GREEN_PIN, 0) #green LED on
				###

				print "TEMP RELAY MODE"
				
				### stop AUTO mode
				os.system("sudo kill -s SIGTERM %d" % TEMP_PID)  #kill child process
				###

				print "killed AUTO MODE %d" % TEMP_PID	

				### Create a child process to control relay
				TEMP_REL_PID=os.fork()
			#	os.waitpid(TEMP_PID,0)

				if TEMP_REL_PID==0:
					print "temp relay"
					RUN_TEMP_REL()
					exit()
				###

				time.sleep(0.5)
		
		#HUMID control
		if GPIO.input(HUMID_BUTTON_PIN)==0 or LOAD_VAL(in_inter, "humid")==1:
			
			### Load humid counter and update on json 
			HUMID_CNT = LOAD_VAL(in_counter,"humid") + 1

			UPDATE_JSON("humid", HUMID_CNT)

			###

			print "HUMID button pressed!"

			if (HUMID_CNT % 3) == 1:
			
				print "Humid sensing mode!"
				
				### Blue LED on
				GPIO.output(HUMID_BLUE_PIN, True)
				###

				### Create a child process for sensing
				HUMID_SEN_PID = os.fork()

				if HUMID_SEN_PID == 0:
					RUN_HUMID_SEN()
					exit()
				###

				time.sleep(0.5)

			elif (HUMID_CNT % 3) == 2:
				if in_rel_on["ON"]["humid"]==1:
					in_rel_int["interrupt"]["humid"]=1
					WRITE_REL_JSON()
				
					while in_rel_on["ON"]["humid"]:
						LOAD_REL_JSON()

				print "HUMID Automode on!"
			
				### Blue LED off / Green LED on
				GPIO.output(HUMID_BLUE_PIN, 0) #Blue LED off
				GPIO.output(HUMID_GREEN_PIN, True) #Green LED on
				###
		
				### stop Sensing and Relay control
				os.system("sudo kill -s SIGTERM %d" % HUMID_SEN_PID)
				os.system("sudo kill -s SIGTERM %d" % HUMID_REL_PID)
				###

				### Create a child process for AUTO mode
				HUMID_PID = os.fork()

				if HUMID_PID == 0:
					RUN_HUMID()
					exit()
				###

				time.sleep(0.5)
		
			else:
				print "HUMID OFF!"
				
				### Green LED off
				GPIO.output(HUMID_GREEN_PIN, 0) #Green LED off
				###

				### stop AUTO mode
				os.system("sudo kill -s SIGTERM %d" % HUMID_PID)
				###

				print "killed child process %d" % HUMID_PID
				
				### Create a child process for relay control
				HUMID_REL_PID = os.fork()
				
				if HUMID_REL_PID == 0:
					RUN_HUMID_REL()
					exit()
				###

				time.sleep(0.5)

		# DUST control
		if GPIO.input(DUST_BUTTON_PIN)==0 or LOAD_VAL(in_inter,"dust")==1:
	
			### Load dust counter and update on json 
			DUST_CNT = LOAD_VAL(in_counter,"dust") + 1

			UPDATE_JSON("dust", DUST_CNT)

			###

			print "DUST button pressed!"

			if (DUST_CNT % 3) == 1:
				print "DUST sensing only!(and relay)"

				### Blue LED on
				GPIO.output(DUST_BLUE_PIN, True)
				###

				### Create a child process for sensing
				DUST_SEN_PID = os.fork()	

				if DUST_SEN_PID == 0:
					RUN_DUST_SEN()			
					exit()
				###

				time.sleep(0.5)

			elif (DUST_CNT % 3) == 2:
				LOAD_REL_JSON()
				
				if in_rel_on["ON"]["dust"]==1:
					in_rel_int["interrupt"]["dust"]=1
					WRITE_REL_JSON()
				
					while in_rel_on["ON"]["dust"]:
						LOAD_REL_JSON()

				#print "DUST auto-mode on!"

				### Blue LED off / Green LED on
				GPIO.output(DUST_BLUE_PIN, 0)	# Blue LED off
				GPIO.output(DUST_GREEN_PIN, 1)	# Green LED on
				###

				### Stop Sensing and Relay control
				os.system("sudo kill -s SIGTERM %d" %DUST_REL_PID)
				os.system("sudo kill -s SIGTERM %d" %DUST_SEN_PID)
				###

				### Create a child process for AUTO mode
				DUST_PID = os.fork()

				if DUST_PID == 0:
					RUN_DUST()
					exit()
				###

				time.sleep(0.5)

			else:
				print "Auto-mode off"
				
				### Green LED off
				GPIO.output(DUST_GREEN_PIN, False)	# Green LED off
				###

				### Stop Auto mode
				os.system("sudo kill -s SIGTERM %d" % DUST_PID)  #kill child process
				###

				print "killed child process %d" % DUST_PID	
			
				### Create a child process to control Relay
				DUST_REL_PID=os.fork()

				if DUST_REL_PID==0:
					RUN_DUST_REL()
					exit()
				###

				time.sleep(0.5)

		# PIR control
		if GPIO.input(PIR_BUTTON_PIN)==0 or LOAD_VAL(in_inter, "pir")==1:
			
			### Load pir counter and update on json 
			PIR_CNT = LOAD_VAL(in_counter,"pir") + 1

			UPDATE_JSON("pir", PIR_CNT)
			###

			print "PIR button pressed! counter: %d"%PIR_CNT

			if (PIR_CNT % 2) == 1:
				print "PIR on!"

				### Blue LED on
				GPIO.output(PIR_LED_PIN, True)	# LED on
				###

				### Create a child process for PIR sensor
				PIR_PID = os.fork()	

				if PIR_PID == 0:
					RUN_PIR()			
					exit()
				###

				time.sleep(0.5)

			else:
				print "PIR off!"

				### Blue LED off
				GPIO.output(PIR_LED_PIN, False)	#LED off
				###

				### Stop sensing
				os.system("sudo kill -s SIGTERM %d" % PIR_PID)  #kill child process
				###
				
				print "killed child process %d" % PIR_PID	
				
				time.sleep(0.5)
		
		time.sleep(1);

except KeyboardInterrupt:
	### Stop running Extra relay control
	os.system("sudo kill -s SIGTERM %d" %EXTRA_PID)
	###

	print "BYE!!"

	#execfile("clean.py")
	GPIO.cleanup()
