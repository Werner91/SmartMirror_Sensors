#Libraries
import RPi.GPIO as GPIO
import time
from subprocess import call
import os
import subprocess

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 22
GPIO_ECHO = 27

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

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

        #bool_ein = os.system('tvservice -s|grep 0x12000a')
	bool_ein = bool subprocess.check_output("tvservice -s|grep '0x12000a'", shell=True)
	streamdata = bool_ein.communicate()[0]
        print("%s" % bool_ein.returncode)

	if distance < 15.0 and distance > 0.0:
            #if (call(["tvservice -s", "|", "grep -q", "state 0x12000a"])) is True:
            if  (bool_ein):  
                print("Monitor wird ausgeschaltet----------------------------------")
                #call(["tvservice", "-o"])
            elif (os.system('tvservice -s | grep -q "state 0x120002"')) is True:
            #elif (call(["tvservice", "-s", "|", "grep", "-q", "state 0x12000a"])) is True:
                #call(["tvservice", "--preferred", ">", "/dev/null;", "fbset" "-depth", "8;", "fbset" "-depth", "16;", "xrefresh;"])
                print("Monitor wird eingeschaltet----------------------------------")
            return distance
        else:
            return 0.0

if __name__ == '__main__':
	try:
		while True:
			dist = distance()
			print ("Measured Distance = %.1f cm" % dist)
			time.sleep(1)

		# Reset by pressing CTRL + C
	except KeyboardInterrupt:
		print("Measurement stopped by User")
		GPIO.cleanup()
