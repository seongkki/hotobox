import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


GPIO.setup(16, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

while True:
	try:
		GPIO.output(19, 1)
		GPIO.output(20, 0)
		GPIO.output(16, 1)
		GPIO.output(26, 1)
		GPIO.output(20, 1)
		GPIO.output(21, 1)
	
	except KeyboardInterrupt:
		GPIO.cleanup()


