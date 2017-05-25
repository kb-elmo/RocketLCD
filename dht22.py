#!/usr/bin/python3
import Adafruit_DHT as dht

sensor = dht.DHT22
pin = 4

def get_data():
   humr, tempr = dht.read_retry(sensor, pin)
   temp = "{:.1f}".format(tempr)
   hum = "{:.1f}".format(humr)
   return temp, hum
