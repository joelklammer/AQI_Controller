#!/usr/bin/python

# constants
THRESHOLD = 100
HYSTERESIS = 10

import socket
from urllib2 import Request, urlopen, URLError, HTTPError
import pibrella 
from time import sleep, strftime, gmtime

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

# Main Function definition
def checkdata():
  req = Request('http://aqi.concordiashanghai.org/data.txt')
  try:
      response = urlopen(req,None,10)
  except HTTPError as e:
      print 'The server aqi.concordiashanghai.org couldn\'t fulfill the request.'
      print 'Error code: ', e.code
      return False;
  except URLError as e:
      print 'We failed to reach aqi.concordiashanghai.org.'
      print 'Reason: ', e.reason
      return False;
  else:
      data = int(float(response.read()))
      print 'New data is', data
    
      # read old_data.txt
      try:
        f = open("/home/pi/old_data.txt", "r")
        try:
          text = f.read()
          old_data = int(float(text))
        finally:
          f.close()
      except IOError:
        print("Failed to read old data")
        pass
      print 'Old data is', old_data

      # Write new data to old_data.txt
      try:
        f = open("/home/pi/old_data.txt", "w")
        try:
          f.write(str(data))
        finally:
          f.close()
      except IOError:
        print("Failed to write old data")
        pass

      if (data >= THRESHOLD) or ((old_data >= THRESHOLD) and (data >= (THRESHOLD - HYSTERESIS))): 
        # print("Controller on")
        pibrella.light.red.on()
        pibrella.light.green.off()
        pibrella.output.e.on()
      else:
        # print("Controller off")
        pibrella.light.red.off()
        pibrella.light.green.on()
        pibrella.output.e.off()
  return True;
# End of Check Data function

checkdata()
while True:
  pibrella.light.amber.fade(0,100,0.4)
  sleep(0.5)
  pibrella.light.amber.fade(100,0,0.4)
  sleep(0.5)
  s = int(float(strftime("%S", gmtime())))
  m = int(float(strftime("%M", gmtime())))
  # print m,':',s
  if (m == 50) and (s == 0):
    successful = False
    count = 0
    while (not successful) and (count < 5):
      successful = checkdata()
      sleep(1)
      count = count + 1
