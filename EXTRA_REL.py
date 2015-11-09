import RPi.GPIO as GPIO
import time
import json

sensor="extra"

REL_PIN=21

GPIO.setmode(GPIO.BCM)

GPIO.setup(REL_PIN, GPIO.OUT)

GPIO.output(REL_PIN, GPIO.HIGH)

### JSON file functions

# rel_on.json
def LOAD_ON_JSON():
        in_file = open("rel_on.json", "r")
        global in_on
        while True:
		try:
			in_on = json.load(in_file)
        		break
		except:
			print "[EXTRA_on] Loading error"
	
	in_file.close()

def WRITE_ON_JSON():
	out_file = open("rel_on.json", "wb")	
	json.dump(in_on, out_file, indent=4)
	out_file.close()

# rel_int.json
def LOAD_INT_JSON():
	in_file = open("rel_int.json", "r")
	global in_int
	while True:
		try:
			in_int = json.load(in_file)
        		break
		except:
			print "[EXTRA_int] Loading error"
	in_file.close()

def WRITE_INT_JSON():
	out_file = open("rel_int.json", "wb")
	json.dump(in_int, out_file, indent=4)
	out_file.close()

# Update json files
def UPDATE_JSON(val):
	global sensor
	in_int["interrupt"]["%s"%sensor]=0
	in_on["ON"]["%s"%sensor]=val


def INIT_JSON():
	global sensor
	in_int["interrupt"]["%s"%sensor]=0
	WRITE_INT_JSON()
	in_on["ON"]["%s"%sensor]=0
	WRITE_ON_JSON()



try:
	### Initialization
	LOAD_ON_JSON()
	LOAD_INT_JSON()
	in_on["ON"]["%s"%sensor]=0
	WRITE_ON_JSON()
	in_int["interrupt"]["%s"%sensor]=0
	WRITE_INT_JSON()
	###
	
	while True:

		LOAD_ON_JSON()
		LOAD_INT_JSON()

		interrupt=in_int["interrupt"]["%s"%sensor]
		ON = in_on["ON"]["%s"%sensor]

		### if there was an interrupt from the web
		### turn LED on/off according to 'ON' attribute
		if interrupt == 1 and ON == 0:
			GPIO.output(REL_PIN, 0)
			print "ON"

			UPDATE_JSON(1)
			WRITE_ON_JSON()
			WRITE_INT_JSON()

		elif interrupt == 1 and ON == 1:
			GPIO.output(REL_PIN, 1)
			print "OFF"
				
			UPDATE_JSON(0)
			WRITE_ON_JSON()
			WRITE_INT_JSON()
		###


		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()

