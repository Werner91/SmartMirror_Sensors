#Libraries
import RPi.GPIO as GPIO
import time
from subprocess import call
import subprocess

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 22
GPIO_ECHO = 27

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#Distance
MAX_DIST = 15.0
MIN_DIST = 0.0

def distance():
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()

	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
	    StartTime = time.time()

	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
	    StopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2

        #check monitor status
	bool_on_off = subprocess.check_output(["tvservice", "-s"])
        
        #Turning monitor on/off if there is something in the right distance
	if distance < MAX_DIST and distance > MIN_DIST:
            if  (bool_on_off.find("12000a") > -1):
                call(["tvservice", "-o"])
                print("Powering monitor off")
                time.sleep(0.5)
            elif (bool_on_off.find("120002") > -1):
                call(["tvservice", "-p"])
                call(["fbset", "-depth", "8"])
                call(["fbset", "-depth", "16"])
                call(["xrefresh"])
                print("Powering monitor on")
            return distance
        else:
            return 0.0

if __name__ == '__main__':
	try:
		while True:
			dist = distance()
			if dist <= MAX_DIST and dist > MIN_DIST: 
                                print("Measured Distance = %.1f cm" % dist)
                                print("\n")
			time.sleep(1)

		# Reset by pressing CTRL + C
	except KeyboardInterrupt:
		print("Measurement stopped by User")
		GPIO.cleanup()
