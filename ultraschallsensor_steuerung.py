#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
from pykeyboard import PyKeyboard
from subprocess import call
import subprocess

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
GPIO_TRIGGER_RECHTS = 18
GPIO_TRIGGER_LINKS= 17
GPIO_ECHO_RECHTS = 24
GPIO_ECHO_LINKS = 23

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_LINKS, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER_RECHTS, GPIO.OUT)
GPIO.setup(GPIO_ECHO_RECHTS, GPIO.IN)
GPIO.setup(GPIO_ECHO_LINKS, GPIO.IN)


#Instanz von PyKeyBoard erstellen
k = PyKeyboard()

#Distance
MAX_DIST = 12.0
MIN_DIST = 0.0

#Testausagbe
print("Script startet") 

def distanzRechts():
	# setze Trigger auf HIGH
	GPIO.output(GPIO_TRIGGER_RECHTS, True)

	# setze Trigger nach 0.01ms auf LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER_RECHTS, False)

	StartZeit_RECHTS = time.time()
	StopZeit_RECHTS = time.time()

	# speichere Startzeit des rechten sensors
	while GPIO.input(GPIO_ECHO_RECHTS) == 0:
		StartZeit_RECHTS = time.time()



	# speichere Ankunftszeit des rechten sensors
	while GPIO.input(GPIO_ECHO_RECHTS) == 1:
		StopZeit_RECHTS = time.time()


	# Zeit Differenz zwischen Start und Ankunft des rechten sensors
	TimeElapsed_RECHTS = StopZeit_RECHTS - StartZeit_RECHTS
	# mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
	# und durch 2 teilen, da hin und zurueck
	distanz_RECHTS = (TimeElapsed_RECHTS * 34300) / 2

	if distanz_RECHTS < MAX_DIST and distanz_RECHTS > MIN_DIST:
		#Kommando um ein Tab weiter zu springen
		k.press_key(k.control_l_key)
		k.tap_key(k.tab_key)
		k.release_key(k.control_l_key)
		return distanz_RECHTS	
	else:
		return 0.0


def distanzLinks():
	# setze Trigger auf HIGH
	GPIO.output(GPIO_TRIGGER_LINKS, True)

	# setze Trigger nach 0.01ms auf LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER_LINKS, False)

	StartZeit_LINKS = time.time()
	StopZeit_LINKS = time.time()

	# speichere Startzeit des linken sensors
	while GPIO.input(GPIO_ECHO_LINKS) == 0:
		StartZeit_LINKS = time.time()



	# speichere Ankunftszeit des linken sensors
	while GPIO.input(GPIO_ECHO_LINKS) == 1:
		StopZeit_LINKS = time.time()


	# Zeit Differenz zwischen Start und Ankunft des linken sensors
	TimeElapsed_LINKS = StopZeit_LINKS - StartZeit_LINKS
	# mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
	# und durch 2 teilen, da hin und zurueck
	distanz_LINKS = (TimeElapsed_LINKS * 34300) / 2


	if distanz_LINKS < MAX_DIST and distanz_LINKS > MIN_DIST:
		#Kommando um ein Tab zurueck zu springen
               	k.press_key(k.control_l_key)
		k.press_key(k.shift_l_key)
                k.tap_key(k.tab_key)
                k.release_key(k.control_l_key)
		k.release_key(k.shift_l_key)
                return distanz_LINKS
		
	else:
		return 0.0



if __name__ == '__main__':
        try:
                while True:
                        #check monitor status
                        bool_on_off = subprocess.check_output(["tvservice", "-s"])
                        if  (bool_on_off.find("12000a") > -1): #monitor is on
                                abstandRechts = distanzRechts()
                                abstandLinks = distanzLinks()
                                if ((abstandRechts > MIN_DIST or abstandLinks > MIN_DIST) and (abstandRechts < MAX_DIST or abstandLinks < MAX_DIST)):
                                        print ("Gemessene Entfernung rechts = %.1f cm" % abstandRechts)
                                        print ("Gemessene Entfernung links = %.1f cm" % abstandLinks)
                                        print ("\n")
                                        time.sleep(1)
                        elif (bool_on_off.find("120002") > -1):
                                #monitor is off - do nothing
                                time.sleep(1)
                                
                #Beim Abbruch durch STRG+C resetten
        except KeyboardInterrupt:
                print("Messung vom User gestoppt")
                GPIO.cleanup()
