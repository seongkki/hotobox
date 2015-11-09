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
import os
import serial
import Adafruit_DHT
import gspread
import ast


# Google Docs account email, password, and spreadsheet name.
GDOCS_EMAIL            = 'psuchefs@gmail.com'
GDOCS_PASSWORD         = 'rydbr12!'
GDOCS_SPREADSHEET_NAME = 'HUMID'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS = 300000
HUMID_ON = 0

#Arduino Port
port="/dev/DHT"
serialFromArduino=serial.Serial(port, 9600)

def login_open_sheet(email, password, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		gc = gspread.login(email, password)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except:
		print 'Unable to login and get spreadsheet.  Check email, password, spreadsheet name.'
		sys.exit(1)


print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'
worksheet = None
while True:
	# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)
	
	# Attempt to get sensor reading.
	#humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
	DHT_ARD=serialFromArduino.readline()
	print DHT_ARD
	s=DHT_ARD.partition(" ")
	humidity = None
	try:
		humidity=int(s[2])
		print humidity
	except:
		print "fail"
	
	
	# Skip to the next reading if a valid measurement couldn't be taken.
	# This might happen if the CPU is under a lot of load and the sensor
	# can't be reliably read (timing is critical to read the sensor).
	if humidity is None:
		print "none"
		time.sleep(2)
		continue

	else:
		print 'Humidity: {0:0.1f} C'.format(humidity)

	# Append the data in the spreadsheet, including a timestamp
		try:
			worksheet.append_row((datetime.datetime.now(), humidity))
		except:
		# Error appending data, most likely because credentials are stale.
		# Null out the worksheet so a login is performed at the top of the loop.
			print 'Append error, logging in again'
			worksheet = None
			time.sleep(FREQUENCY_SECONDS)
			continue

		# Wait 30 seconds before continuing
		print 'Wrote humidity row to {0}'.format(GDOCS_SPREADSHEET_NAME)
		time.sleep(FREQUENCY_SECONDS)	
