import RPi.GPIO as GPIO 
import time
from urllib.request import urlopen
import sys

WRITE_API = "AUM55XWM4XZN4BN8" # Replace your ThingSpeak API key here
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)

ThingSpeakPrevSec = 0
ThingSpeakInterval = 20

GPIO.setmode (GPIO.BOARD)

GPIO_TRIGGER=32
GPIO_ECHO=36
PIR=35
LDR=40
LED=38


GPIO.setup (GPIO_TRIGGER, GPIO.OUT)
GPIO.setup (GPIO_ECHO, GPIO.IN)
GPIO.setup (PIR, GPIO.IN)
GPIO.setup (LDR, GPIO.IN)
GPIO.setup (LED, GPIO.OUT)

def distance():

 GPIO.output(GPIO_TRIGGER,True)
 time.sleep(0.00001)
 GPIO.output(GPIO_TRIGGER,False)
 StartTime=time.time()
 StopTime=time.time()
 while GPIO.input (GPIO_ECHO)==0:
       StartTime=time.time()
 while GPIO.input (GPIO_ECHO)==1:
       StopTime=time.time()
 TimeElapsed=StopTime-StartTime
 distance=(TimeElapsed*34300)/2
 return distance

if '___name___'=='__main__':
 time.sleep(1)
try:
    while True:
     if (GPIO.input(PIR)==0):
         dist=distance()
         SensorPrevSec = distance()
            
         thingspeakHttp = BASE_URL + "&field1={:.2f}".format(dist)
         print(thingspeakHttp)
            
         conn = urlopen(thingspeakHttp)
         print(dist)
         if (dist<50):
                if (GPIO.input(LDR)==0):
                    GPIO.output(LED,True)
                    print ("Intruder Detected")
                    time.sleep(0.01)
     if (GPIO.input(PIR)==1):
         GPIO.output(LED,False)
         print ("Intruder not Detected")
         time.sleep(0.01)
        

except KeyboardInterrupt:
  print ("MEASUREMENT STOPPED BY USER")
  GPIO.cleanup()
