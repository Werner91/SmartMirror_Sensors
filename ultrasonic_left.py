#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
from pykeyboard import PyKeyboard
from subprocess import call
import subprocess


#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins
GPIO_TRIGGER_LINKS= 17
GPIO_ECHO_LINKS = 23

#Direction GPIO-Pins (IN / OUT)
GPIO.setup(GPIO_TRIGGER_LINKS, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LINKS, GPIO.IN)


#Instance of PyKeyBoard
k = PyKeyboard()

#Distance
MAX_DIST = 16.0
MIN_DIST = 0.0



#Teststring
print("Left senor script startet") 


def distanzLinks():

        GPIO.output(GPIO_TRIGGER_LINKS, False)
        time.sleep(0.1)
	# set Trigger on HIGH
	GPIO.output(GPIO_TRIGGER_LINKS, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER_LINKS, False)

	timeout = time.time() + (2*(MAX_DIST/100)/(343))
	# save Starttime of the left sensors
	while GPIO.input(GPIO_ECHO_LINKS) == 0:
                if(time.time() > timeout):
                        break
                # This is to prevent to get stuck in this loop
                # This is a Bug of the SR-04 Ultrasonicsensor
                # If there is a SRF-05 used in stead if a SR-04 his 3 lines can be removed
                # GPIO.setup(GPIO_ECHO_LINKS, GPIO.OUT)
                # GPIO.output(GPIO_ECHO_LINKS, False)
                # GPIO.setup(GPIO_ECHO_LINKS, GPIO.IN)
                pass
        StartZeit_LINKS = time.time()


	# save Stoptime of the left sensors
	while GPIO.input(GPIO_ECHO_LINKS) == 1:
                pass
	StopZeit_LINKS = time.time()
        
	# time difference between start and arrival of the right sensors
	TimeElapsed_LINKS = StopZeit_LINKS - StartZeit_LINKS
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distanz_LINKS = (TimeElapsed_LINKS * 34300) / 2
        print("%s \n" % distanz_LINKS)

	if distanz_LINKS < MAX_DIST and distanz_LINKS > MIN_DIST:
		#Command to jump to previous browsertab
               	k.press_key(k.control_l_key)
		k.press_key(k.shift_l_key)
                k.tap_key(k.tab_key)
                k.release_key(k.control_l_key)
		k.release_key(k.shift_l_key)
                return distanz_LINKS
		
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
                                abstandLinks = distanzLinks()
                                if (abstandLinks > MIN_DIST and abstandLinks < MAX_DIST):
                                        print ("Measured Distance left = %.1f cm" % abstandLinks)
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
