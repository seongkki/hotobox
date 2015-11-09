import sys
import time
import datetime
import serial
import gspread
import RPi.GPIO as io
import RPi.GPIO as GPIO
import io
import json 

#google account
GDOCS_EMAIL = 'psuchefs@gmail.com'
GDOCS_PASSWORD = 'rydbr12!'
GDOCS_SPREADSHEET_NAME = 'DUST'

#How long to wait (in seconds) between measurements
FREQUENCY_SECONDS = 10
DUST_ON = 0

#Arduino Port
port="/dev/DUST"
serialFromArduino=serial.Serial(port, 9600)

pin=18

#Relay GPIO Setup	
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH)

def login_open_sheet(email, password, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet"""
	try:
		gc = gspread.login(email, password)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except:
		print 'Unable to login and get spreadsheet. Check email, password, spreadsheet name.'
#		sys.exit(1)

### JSON file
def LOAD_JSON():
	in_file=open("inter.json", "r")
	global in_data
	while True:
		try:
			in_data=json.load(in_file)
			break
		except:
			print "[DUST AUTO] Loading Error"

### JSON file
def LOAD_REL_JSON():
	in_file=open("rel_on.json", "r")
	global in_rel
	while True:
		try:
			in_rel=json.load(in_file)
			break
		except:
			print "[DUST AUTO] Loading Error"

###
def WRITE_REL_JSON():
	out_file=open("rel_on.json", "wb")
	json.dump(in_init, out_file, indent=4)
	out_file.close()


print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl+c to quit.'
worksheet = None

while True:
	
	LOAD_JSON()

	setting = in_data["set"]["dust"]

	if setting <= 0:
		setting = 100

	#Login if necessary
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)

	#Attempt to get sensor reading
	dust=0

	while dust==0:
		try:
 		    	dust=int(serialFromArduino.readline())
		except:
			print "fail"

	LOAD_REL_JSON()

        if (dust>setting):
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1)
            DUST_ON = 1
	    in_rel["ON"]["dust"]=1

        else:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1)
            DUST_ON = 0
	    in_rel["ON"]["dust"]=0

	WRITE_REL_JSON()
	

	#Skip to the next reading if a valid measurement couldn't be taken.
	#This might happen if the CPU is under a lot of load and the sensor
	#can't be reliably read (timing is critical to read the sensor).

	if dust is None:
		time.sleep(2)
		continue

	print 'Dust Value: {0:0.1f}'.format(dust)

	#Append the data in the spreadsheet including a timestamp

	try:
		worksheet.append_row((datetime.datetime.now(), dust))
	except:
		#Error appending data, most likely because credentials are stable.
		#Null out the worksheet so login is performed at the top of the loop.
		print 'Append error, logging in again'
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	#wait 30 seconds before continuing
	print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
	time.sleep(FREQUENCY_SECONDS)
