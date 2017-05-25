#!/usr/bin/python3
import RPi.GPIO as GPIO
import os
import time
import lcddriver

GPIO.setmode(GPIO.BCM)

GPIO.setup(11, GPIO.OUT)
GPIO.output(11, True)
GPIO.setup(17, GPIO.IN)

time.sleep(5)

while True:
   if not GPIO.input(17):
      GPIO.output(11, False)
      time.sleep(0.2)
      GPIO.output(11, True)
      time.sleep(0.2)
      GPIO.output(11, False)
      time.sleep(0.2)
      GPIO.output(11, True)
      time.sleep(2)
      os.system("sudo systemctl stop rocketlcd")
      time.sleep(1)
      lcd = lcddriver.lcd(0x26)
      lcd.display_line("Bye Bye", 1, "c", 16)
      time.sleep(5)
      os.system("sudo shutdown -h now")
   time.sleep(5)
