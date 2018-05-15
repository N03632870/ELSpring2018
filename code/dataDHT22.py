
import Adafruit_DHT as dht import RPi.GPIO as GPIO import time import os 
import sys import sqlite3 as mydb import paho.mqtt.client as mqtt 
GPIO.setmode(GPIO.BCM) GPIO.setup(17,GPIO.OUT) def Blink():
  for i in range(0,2):
    print("Blink #" + str(i+1))
    GPIO.output(17,True)
    time.sleep(1)
    GPIO.output(17,False)
    time.sleep(1)
  print("Done!!")
  GPIO.cleanup() Blink() def readTemp():
   h,t = dht.read_retry(dht.DHT22, 27)
   F = 9.0/5.0 * t + 32
   
   print 'Temp={0:0.1f}*c Humidity={1:0.1f}%'.format(F,h)
   return [F,h]
#def logTemp():
#   con = mydb.connect('/home/pi/ELSpring2018/code/Database/dth22.db') 
#   with con:
#      try:
#         [t,F,H]=readTemp() print "Current temperature is: %s F" %F cur 
#         = con.cursor()
         #sql = "insert into TempData values(?,?,?)"
#         cur.execute('insert into data01 values(?,?,?)',(t,F,H)) print 
#      "Temperature logged" except:
#         print "Error" logTemp()
[F,H]=readTemp() client = mqtt.Client() 
client.connect("192.168.43.51",1883,60) client.publish("table", 
"Data02"); client.publish("temperature", F); client.publish("humidity", 
H); client.disconnect();
print "complete"
