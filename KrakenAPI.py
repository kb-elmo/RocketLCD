#!/usr/bin/python
import json
import urllib.request

api_url = "https://api.kraken.com/0/public/Ticker"

def api_get(pair):
   req = urllib.request.Request(api_url+"?pair="+pair)
   res = urllib.request.urlopen(req).read()
   json_data = json.loads(res.decode('UTF-8'))["result"]
   pair = list(json_data.keys())[0]
   return json_data[pair]

def get_ask(json_data):
   ask = "{:.2f}".format(float(json_data["a"][0]))
   return str(ask)

def get_bid(json_data):
   bid = "{:.2f}".format(float(json_data["b"][0]))
   return str(bid)

def get_volume(json_data):
   vol = int(float(json_data["v"][1]))
   return str(vol)

def get_last(json_data):
   last = "{:.2f}".format(float(json_data["c"][0]))
   return str(last)

def get_low(json_data):
   low = "{:.2f}".format(float(json_data["l"][0]))
   return str(low)

def get_high(json_data):
   high = "{:.2f}".format(float(json_data["h"][0]))
   return str(high)

