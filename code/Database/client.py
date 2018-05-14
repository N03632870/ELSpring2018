#!/usr/bin/env python

from time import strftime
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import sqlite3
import time

topic_table="table"
topic_temp = "temperature"
topic_hum= "humidity"
dbFile = "dth22.db"

dataTuple = [-1,-1]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_table)
    client.subscribe(topic_temp)
    client.subscribe(topic_hum)
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    theTime = strftime("%m/%d/%Y %X")
    global table
    result = (theTime + "\t" + str(msg.payload))
    print(msg.topic + ":\t" + result)
    if (msg.topic == topic_table):
        table = str(msg.payload)
    if (msg.topic == topic_temp):
        dataTuple[0] = str(msg.payload)
    if (msg.topic == topic_hum):
        dataTuple[1] = str(msg.payload)
        #return
    if (dataTuple[0] != -1 and dataTuple[1] != -1):
        writeToDb(table, theTime, dataTuple[0], dataTuple[1])
    return

def writeToDb(table, theTime, temperature, humidity):
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    print "Writing to db..."
    print ("INSERT INTO "+ table + " VALUES (?,?,?)", (theTime, temperature, humidity))
    c.execute("INSERT INTO "+ table + " VALUES (?,?,?)", (theTime, temperature, humidity))
    conn.commit()
    Blink()
    global dataTuple
    dataTuple = [-1, -1]

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
def Blink():
  for i in range(0,1):
    print("Blink #" + str(i+1))
    GPIO.output(17,True)
    time.sleep(1)
    GPIO.output(17,False)
    time.sleep(1)
  print("Done!!")
  #GPIO.cleanup()
Blink()
    
client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
