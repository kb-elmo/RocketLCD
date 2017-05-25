#!/usr/bin/python3
import json
import urllib.request
import datetime
import pytz

API_URL = "https://launchlibrary.net/1.2/launch/next/1"

def api_request():
   request = urllib.request.Request(API_URL)
   response = urllib.request.urlopen(request).read()
   json_data = json.loads(response.decode('UTF-8'))
   return json_data['launches'][0]

def full_name(json_data):
   name = json_data['name']
   return name

def rocket_name(json_data):
   name = json_data['rocket']['name']
   return name

def mission_name(json_data):
   name = json_data['missions'][0]['name']
   return name

def window_open(json_data):
   time_utc_string = json_data['windowstart']
   time_utc = datetime.datetime.strptime(time_utc_string, '%B %d, %Y %H:%M:%S %Z')
   time_local = pytz.utc.localize(time_utc).astimezone(pytz.timezone('Europe/Berlin'))
   time = datetime.datetime.strftime(time_local, '%d-%m-%Y %H:%M:%S')
   return time

def net_raw_utc(json_data):
   time_utc_string = json_data['net']
   time_utc = datetime.datetime.strptime(time_utc_string, '%B %d, %Y %H:%M:%S %Z')
   return time_utc

def net(json_data):
   time_utc_string = json_data['net']
   time_utc = datetime.datetime.strptime(time_utc_string, '%B %d, %Y %H:%M:%S %Z')
   time_local = pytz.utc.localize(time_utc).astimezone(pytz.timezone('Europe/Berlin'))
   time = datetime.datetime.strftime(time_local, 'NET %d.%m.%Y')
   return time

def window_close(json_data):
   time_utc_string = json_data['windowend']
   time_utc = datetime.datetime.strptime(time_utc_string, '%B %d, %Y %H:%M:%S %Z')
   time_local = pytz.utc.localize(time_utc).astimezone(pytz.timezone('Europe/Berlin'))
   time = datetime.datetime.strftime(time_local, '%d-%m-%Y %H:%M:%S')
   return time

def time_to_launch(json_data):
   launch_time_string = json_data['net']
   launch_time_utc = datetime.datetime.strptime(launch_time_string, '%B %d, %Y %H:%M:%S %Z')
   utc_now = datetime.datetime.utcnow().replace(microsecond=0)
   timedelta = launch_time_utc - utc_now
   return timedelta

def is_tbd(json_data):
   tbd_status = json_data['tbdtime']
   if tbd_status == 1:
      return True
   else:
      return False

def is_go(json_data):
   status = json_data['status']
   if status == 1:
      return True
   else:
      return False

def in_hold(json_data):
   hold_state = json_data['inhold']
   if hold_state == 1:
      return True
   else:
      return False

def launch_pad(json_data):
   pad = json_data['location']['pads'][0]['name']
   return pad

