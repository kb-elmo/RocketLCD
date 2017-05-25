#!/usr/bin/python3
import threading
import datetime
import KrakenAPI as kraken
import LaunchAPI as launch
import dht22 as dht
import RPi.GPIO as gpio
import lcddriver
import socket
import logging
from time import sleep
from string import Template

logging.basicConfig(level=logging.INFO)

gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT)
gpio.output(24, True)
sleep(1)
gpio.output(24, False)

lcd2 = lcddriver.lcd(0x26)
lcd1 = lcddriver.lcd(0x27)

def get_IP():
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   sock.connect(("8.8.8.8", 80))
   ip_address = sock.getsockname()[0]
   sock.close()
   return ip_address

def wait_for_network():
   while True:
      try:
         IP = get_IP()
         lcd1.clear()
         lcd1.display_line("IP-Address", 2, "c", 20)
         lcd1.display_line(str(IP), 3, "c", 20)
         sleep(5)
         break
      except:
         lcd1.display_line("Waiting for", 2, "c", 20)
         lcd1.display_line("Network", 3, "c", 20)
         sleep(10)

def blink_led():
   gpio.output(24, True)
   sleep(1)
   gpio.output(24, False)

lcd2.display_line("Raspbian 8", 1, "c", 16)
lcd2.display_line("Linux 4.4.50", 2, "c", 16)
wait_for_network()
lcd1.clear()
lcd1.display_line("Launch Timer", 2, "c", 20)
lcd1.display_line("v1.5", 3, "c", 20)
sleep(5)
lcd1.clear()
lcd1.display_line("Waiting", 2, "c", 20)
lcd1.display_line("for data", 3, "c", 20)

class Launch_Thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      show_update = 1
      while True:
         counter = 0
         try:
            json_launch = launch.api_request()
         except:
            wait_for_network()
            json_launch = launch.api_request()
         logging.info("Updated Launch-Data")
         blink_led()
         ttl = launch.time_to_launch(json_launch)
         if show_update == 1:
            if ttl < datetime.timedelta(minutes=30):
               update_interval = 60
               update_string = "Next Launch:\n> 30 Minutes\nUpdate Interval:\n1 Minute"
               lcd1.display_string(update_string, "c", 20)
               show_update = 0
               sleep(3)
            elif ttl < datetime.timedelta(hours=1):
               update_interval = 300
               update_string = "Next Launch:\n> 1 Hour\nUpdate Interval:\n5 Minutes"
               lcd1.display_string(update_string, "c", 20)
               show_update = 0
               sleep(3)
            elif ttl < datetime.timedelta(hours=2):
               update_interval = 600
               update_string = "Next Launch:\n> 2 Hours\nUpdate Interval:\n10 Minutes"
               lcd1.display_string(update_string, "c", 20)
               show_update = 1
               sleep(3)
            elif ttl < datetime.timedelta(hours=6):
               update_interval = 900
               update_string = "Next Launch:\n> 6 Hours\nUpdate Interval:\n15 Minutes"
               lcd1.display_string(update_string, "c", 20)
               show_update = 1
               sleep(3)
            else:
               update_interval = 1800
               update_string = "Next Launch:\n< 6 Hours\nUpdate Interval:\n30 Minutes"
               lcd1.display_string(update_string, "c", 20)
               show_update = 1
               sleep(3)
         update_launch_display(json_launch)
         launch_time = launch.net_raw_utc(json_launch)
         if launch.is_tbd(json_launch) is True:
            lcd1.display_line(launch.net(json_launch), 4, "c", 20)
            sleep(update_interval)
         else:   
            while counter <= update_interval:
               now = datetime.datetime.utcnow().replace(microsecond=0)
               if launch_time > now:
                  timedelta = launch_time - now
                  t_string = "-"
               else:
                  timedelta = now - launch_time
                  t_string = "+"
               if timedelta == datetime.timedelta(hours=6) or timedelta == datetime.timedelta(hours=2) or \
               timedelta == datetime.timedelta(hours=1) or timedelta == datetime.timedelta(minutes=30):
                  break
               if counter % 2 == 0:
                  deltastring = strfdelta(timedelta, "T"+t_string+"%D:%H:%M:%S")
               else:
                  deltastring = strfdelta(timedelta, "T %D %H %M %S")
               lcd1.display_line(str(deltastring), 4, "c", 20)
               counter += 1
               sleep(1)

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

def update_launch_display(json_data):
   lcd1.display_line(launch.rocket_name(json_data), 1, "c", 20)
   lcd1.display_line(launch.mission_name(json_data), 2, "c", 20)
   if launch.is_tbd(json_data) is True:
      lcd1.display_line("Status: TBD", 3, "c", 20)
   elif launch.in_hold(json_data) is True:
      lcd1.display_line("Status: HOLD", 3, "c", 20)
   elif launch.is_go(json_data) is False:
      lcd1.display_line("Status: NO-GO", 3, "c", 20)
   else:
      lcd1.display_line("Status: GO", 3, "c", 20)

class Top_LCD_Thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      while True:
         try:
            json_btc = kraken.api_get("XBTEUR")
            last = kraken.get_last(json_btc)
            logging.info("Updated BTC-Data")
         except:
            last = "No Data"
            logging.info("BTC-Data Update failed")
         blink_led()
         cnt = 0
         cntt = 0
         while cnt <= 10:
            while cntt <= 3:
               now = datetime.datetime.now()
               try:
                  temp, hum = dht.get_data()
                  roomstring = str(temp)+"\xDFC  "+str(hum)+"%"
               except:
                  roomstring = "No Data"
               time = datetime.datetime.strftime(now, "%d.%m.%Y %H:%M")
               lcd2.display_line(str(time), 1, "c", 16)
               lcd2.display_line(roomstring, 2, "c", 16)
               cntt += 1
               sleep(15)
            lcd2.display_line("BTC -> EUR", 1, "c", 16)
            lcd2.display_line(str(last), 2, "c", 16)
            cnt += 1
            cntt = 0
            sleep(15)


def main():
   thread1 = Top_LCD_Thread()
   thread2 = Launch_Thread()
   thread1.start()
   sleep(5)
   thread2.start()
   thread1.join()
   thread2.join()

if __name__ == "__main__":
   main()
