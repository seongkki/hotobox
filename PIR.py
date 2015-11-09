import time
import RPi.GPIO as io
import RPi.GPIO as GPIO
import os
import serial
import sys
import json
import picamera

camera=picamera.PiCamera()

pic = 0

def LOAD_JSON():
	in_file = open("inter.json", "r")
	global in_data
	while True:
		try:
			in_data = json.load(in_file)
			print "[PIR_int] Successfully loaded"
			break
		except:
			print "[PIR_int] Loading error"
		
	in_file.close()

def WRITE_JSON():
	out_file = open("inter.json","wb")
	json.dump(in_data, out_file, indent=4)
	out_file.close()

# Arduino Port 
port="/dev/PIR"
serialFromArduino=serial.Serial(port, 9600)

try:
	while True:

		LOAD_JSON()
		try:
			input=int(serialFromArduino.readline())
		except:
			input=0

		if input or in_data["interrupt"]["pir"]==2:
			
			print("motion detected")

			t=time.localtime()

			name = str(t.tm_mon)+"_"+str(t.tm_mday)+"_"+str(t.tm_hour)+"_"+str(t.tm_min)+"_"+str(t.tm_sec)
			
			camera.vflip=True

			camera.capture('./photo/%s.jpg' % name)
			pic = pic + 1
						
			time.sleep(5)
			print ("%s" % name)
			os.system("../GoogleDrive/grive")

			LOAD_JSON()
			in_data["interrupt"]["pir"]=0
			WRITE_JSON()
			
		else:
			print("None")
			time.sleep(0.5)
					
except KeyboardInterrupt:
        io.cleanup()
