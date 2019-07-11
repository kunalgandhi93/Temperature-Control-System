#
# Embedded Systems Project 
# Date:12/12/2017
#
# Author: Kunal Gandhi 
#
# Objectives:
# 1.The Raspberry Pi should be able to sense the value of the sensor using SPI communication.
# 2.The Raspberry Pi should be able to send the value of the sensor to the IBM Bluemix Cloud and display the same on an Android device. 
# 3.The Android phone should be able to control the toy motor remotely.
# 4.The students should be able to create a flow using Node Red Application that gets the sensor values from Raspberry #Pi using MQTT. Email updates should then be sent to the user regarding the sensor values. 
#
#
# Hardware Details: Raspberry Pi 2/3 with NOOBS O.S., DC Motor, Motor Driver-L293D, A/D converter-MCP3008, LM35 Temperature sensor, Breadboard and Connectors, Propeller on motor 
#

import spidev 
from time import sleep
import os
import paho.mqtt.client as mqtt

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
tempChannel = 0

# MQTT connection parameters
client = mqtt.Client("Kunal")
client.connect("localhost")

#Read 10 bit ADC channel 0
def getReading(channel):
  adc = spi.xfer([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

#Scale temperature
def ConvertTemp(temp,places):
  val = ((temp *330)/float(1023))-150
  val = round (val,places)
  return val

#Read ADC values continuosly by polling
while True:
    temp = getReading(tempChannel)
    final_val = ConvertTemp(temp,2)

#Print ADC value on console
    print (final_val)
    client.publish("temp", final_val)
    sleep(1)