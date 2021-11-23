#!/usr/bin/python

import os, datetime, smtplib, socket
from email.mime.text import MIMEText
from time import *
try:
    t = os.path.getmtime('/home/pi/old_data.txt')
except IOError:
    print "failed to get information about old_data.txt"
else:
    v = datetime.datetime.fromtimestamp(t)
    c = datetime.datetime.now()
    filetime = int( v.strftime("%H") )
    systime = int( c.strftime("%H") ) 
    print filetime,systime
    if (systime != filetime):
      to = 'joel.klammer@concordiashanghai.org'
      gmail_user = 'AQI.Concordia@gmail.com' 
      gmail_password = 'xxxxxxxxxxxxxxxx' 
      smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
      smtpserver.ehlo()
      smtpserver.starttls()
      smtpserver.ehlo
      smtpserver.login(gmail_user, gmail_password)
      today = datetime.date.today()
      temp = 'Hello,/n/nThe last update of old_data.txt on the AQI Filter Controller was at ' + str(filetime % 24) + ':50./nThis may be due to a temporary network issue./nIf it continues, it may be an indicator that the AQI Machine located on the HS 4/F Science rooftop is not operating.'
      msg = MIMEText(temp)
      msg['Subject'] = 'The AQI Filter Controller has not updated its data on %s' % today.strftime('%b %d %Y')
      msg['From'] = gmail_user
      msg['To'] = to
      smtpserver.sendmail(gmail_user, [to], msg.as_string())
      smtpserver.quit()
