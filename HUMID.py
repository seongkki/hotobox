#!/usr/bin/python

# Google Spreadsheet DHT Sensor Data-logging Example

# Depends on the 'gspread' package being installed.  If you have pip installed
# execute:
#   sudo pip install gspread

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import datetime
import RPi.GPIO as GPIO
import os
import serial
import Adafruit_DHT
import gspread
import ast
import signal
import json

### Clean up GPIO and exit the program
def sig_handler(signal, frame):
	print "bye bye"
	GPIO.cleanup()
	exit()
###

### Google Docs account email, password, and spreadsheet name.
GDOCS_EMAIL            = 'psuchefs@gmail.com'
GDOCS_PASSWORD         = 'rydbr12!'
GDOCS_SPREADSHEET_NAME = 'HUMID'
###

### How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS = 3
HUMID_ON = 0
###

### Arduino Port
port="/dev/DHT"
serialFromArduino=serial.Serial(port, 9600)
###

### Relay GPIO setup
# Relay pin
REL_PIN=17

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(REL_PIN, GPIO.OUT)
GPIO.output(REL_PIN, GPIO.HIGH)
###

### Logging into gspread
def login_open_sheet(email, password, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		gc = gspread.login(email, password)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except:
		print 'Unable to login and get spreadsheet.  Check email, password, spreadsheet name.'
		sys.exit(1)
###

### JSON FILE
def LOAD_JSON():
        in_file = open("inter.json","r")
	global in_data
	while True:
		try:
			in_data = json.load(in_file)
			print "[HUMID AUTO] Successfully Loaded"
			break
		except:
			print "[HUMID AUTO] Loading Error"
	in_file.close()

### JSON files 
def LOAD_REL_JSON():
	in_file = open("rel_on.json","r")
	global in_rel
	while True:
		try:
			in_rel = json.load(in_file)
			break
		except:
			print"[TEMP REL] Loading Error"
	in_file.close()
	     
def WRITE_REL_JSON():
	out_file=open("rel_on.json","wb")
	json.dump(in_rel, out_file, indent=4)
	out_file.close()


print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'
worksheet = None

while True:

	### Set the humidity from user
	LOAD_JSON()

	setting = in_data["set"]["humid"]

	if setting <= 0:
		setting =25

	### ??? open new sheet if neccessary
	# Log in if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)
	###

	### Parse only humidity part
	# Attempt to get sensor reading.
	#humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
	DHT_ARD=serialFromArduino.readline()
	print DHT_ARD
	s=DHT_ARD.partition(" ")
	humid=None
	###
	
	####################################################################################################

	### catch error on parsing
	try:
		humid = int(s[2])
		print humid
	
	except:
		print "fail"
	###

	
	### Skip to the next reading if a valid measurement couldn't be taken.
	### This might happen if the CPU is under a lot of load and the sensor
	### can't be reliably read (timing is critical to read the sensor).
	if humid is None:
		print "none"
		time.sleep(2)
		continue
	###

	print 'Humidity: {0:0.1f} %'.format(humid)

	### Control the relay according to humid value
	LOAD_REL_JSON()
	
	if (humid > setting):
		### Turning off Relay
		GPIO.output(REL_PIN, GPIO.HIGH)
		###
		HUMID_ON = 0
		in_rel["ON"]["humid"]=0

	else:
		### Turning on Relay
		GPIO.output(REL_PIN, GPIO.LOW)
		###
		HUMID_ON = 1
		in_rel["ON"]["humid"]=1
	
	WRITE_REL_JSON()
	###

	### Append the data in the spreadsheet, including a timestamp
	try:
		worksheet.append_row((datetime.datetime.now(), humid))
	except:
		# Error appending data, most likely because credentials are stale.
		# Null out the worksheet so a login is performed at the top of the loop.
		print 'Append error, logging in again'
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue
	###

	### Handle the signal from the parent
	signal.signal(signal.SIGTERM, sig_handler)
	###

	### Wait 30 seconds before continuing
	print 'Wrote Humidity row to {0}'.format(GDOCS_SPREADSHEET_NAME)
	time.sleep(FREQUENCY_SECONDS)	
	###

############ End############
