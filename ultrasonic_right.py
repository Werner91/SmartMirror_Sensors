#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
from pykeyboard import PyKeyboard
from subprocess import call
import subprocess

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins
GPIO_TRIGGER_RECHTS = 18
GPIO_ECHO_RECHTS = 24

#Direction GPIO-Pins (IN / OUT)
GPIO.setup(GPIO_TRIGGER_RECHTS, GPIO.OUT)
GPIO.setup(GPIO_ECHO_RECHTS, GPIO.IN)


#Instance of PyKeyBoard
k = PyKeyboard()

#Distance
MAX_DIST = 16.0
MIN_DIST = 0.0

#Timeout for while loop



#Teststring
print("Right sensor script startet") 

def distanzRechts():

        GPIO.output(GPIO_TRIGGER_RECHTS, False)
        time.sleep(0.1)
        
	# set Trigger on HIGH
	GPIO.output(GPIO_TRIGGER_RECHTS, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER_RECHTS, False)

        timeout = time.time() + (2*(MAX_DIST/100)/(343))

	# save Starttime of the right sensors
	while GPIO.input(GPIO_ECHO_RECHTS) == 0:
                if(time.time() > timeout):
                        break
                # This is to prevent to get stuck in this loop
                # This is a Bug of the SR-04 Ultrasonicsensor
                # If there is a SRF-05 used in stead if a SR-04 his 3 lines can be removed
                #GPIO.setup(GPIO_ECHO_RECHTS, GPIO.OUT)
                #GPIO.output(GPIO_ECHO_RECHTS, False)
                #GPIO.setup(GPIO_ECHO_RECHTS, GPIO.IN)
                pass
	StartZeit_RECHTS = time.time()

	# save Stoptime of the right sensors
	while GPIO.input(GPIO_ECHO_RECHTS) == 1:
                pass
	StopZeit_RECHTS = time.time()


	# time difference between start and arrival of the right sensors
	TimeElapsed_RECHTS = StopZeit_RECHTS - StartZeit_RECHTS
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distanz_RECHTS = (TimeElapsed_RECHTS * 34300) / 2
	print("%s \n" % distanz_RECHTS)

	if distanz_RECHTS < MAX_DIST and distanz_RECHTS > MIN_DIST:
		#Command to jump to next browsertab
		k.press_key(k.control_l_key)
		k.tap_key(k.tab_key)
		k.release_key(k.control_l_key)
		return distanz_RECHTS	
	else:
		return 0.0



if __name__ == '__main__':
        count = 0
        try:
                while True:
                        count = count + 1
                        print("%d \n" %count)
                        #check monitor status
                        bool_on_off = subprocess.check_output(["tvservice", "-s"])
                        if  (bool_on_off.find("120006") > -1): #monitor is on
                                abstandRechts = distanzRechts()
                                if (abstandRechts > MIN_DIST and abstandRechts < MAX_DIST):
                                        print ("Measured Distance right = %.1f cm" % abstandRechts)
                                        print ("\n\n")
                                time.sleep(1)
                        elif (bool_on_off.find("120002") > -1):
                                #monitor is off - do nothing
                                print("\n monitor is off \n")
                                time.sleep(1)
                        else:
                                print("\n could not determine monitor status \n")
                                time.sleep(1) # to prevent 100% cpu on the looping
    
                # Reset by pressing CTRL + C
        except KeyboardInterrupt:
                print("Measurement stopped by User")
                GPIO.cleanup()
