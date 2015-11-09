import sys
import time
import datetime
import serial
import gspread
import io

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

def login_open_sheet(email, password, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet"""
	try:
		gc = gspread.login(email, password)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except:
		print 'Unable to login and get spreadsheet. Check email, password, spreadsheet name.'
		sys.exit(1)

print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl+c to quit.'
worksheet = None
while True:
	#Login if necessary
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)

	#Attempt to get sensor reading
	while True:
		try:
		     	dust=int(serialFromArduino.readline())
			break
		except:
			print "Reading fail" 
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
