#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
from pykeyboard import PyKeyboard
from subprocess import call
import subprocess
from thread import start_new_thread, allocate_lock

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
MAX_DIST = 12.0
MIN_DIST = 0.0

#lock thread
lock = allocate_lock()


#Teststring
print("Left senor script startet") 


def distanzLinks():
        
	# set Trigger on HIGH
	GPIO.output(GPIO_TRIGGER_LINKS, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER_LINKS, False)


	# save Starttime of the left sensors
	while GPIO.input(GPIO_ECHO_LINKS) == 0:
                pass
    #            print("still in loooooooop left sensor\n")
        StartZeit_LINKS = time.time()


    #    print("passed first loop")

	# save Stoptime of the left sensors
	while GPIO.input(GPIO_ECHO_LINKS) == 1:
                pass
	StopZeit_LINKS = time.time()

		
     #   print("passed second loop")
        
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
                #       print("\n tvservice check %s \n" % bool_on_off)
                        if  (bool_on_off.find("120006") > -1): #monitor is on
                               
                                abstandLinks = distanzLinks()
                #                print("\n left sensor works")                               
                #                print("\n monitor is on \n")
                                
                                
                                if (abstandLinks > MIN_DIST and abstandLinks < MAX_DIST):
                                        print ("Gemessene Entfernung links = %.1f cm" % abstandLinks)
                                        print ("\n\n")
                #                print("done start new messung")
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
                print("Messung vom User gestoppt")
                GPIO.cleanup()
