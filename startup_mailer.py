import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime

def connect_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type

# Change to your own account information
# Account Information
to = 'joel.klammer@concordiashanghai.org' # Email to send to.
gmail_user = 'AQI.Concordia@gmail.com' # Email to send from. (MUST BE GMAIL)
gmail_password = 'xxxxxxxxxxxxxxxxx' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)  # Log in to server
today = datetime.date.today()  # Get current time/date

arg='ip route list'  # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()  # Get data from 'p terminal'.

# Split IP text block into three, and divide the two containing IPs into words.
ip_lines = data[0].splitlines()
split_line_a = ip_lines[1].split()
# split_line_b = ip_lines[2].split()

# con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
ip_type_a = connect_type(split_line_a)
# ip_type_b = connect_type(split_line_b)

"""Because the text 'src' is always followed by an ip address,
we can use the 'index' function to find 'src' and add one to
get the index position of our ip.
"""
ipaddr_a = split_line_a[split_line_a.index('src')+1]
#ipaddr_b = split_line_b[split_line_b.index('src')+1]

# Creates a sentence for each ip address.
my_ip_a = 'Good morning,\n\nThe %s IP Address for the AQI Filtration System Controller is %s' % (ip_type_a, ipaddr_a)
my_ip_b = 'The Controller is located in the 2/F HS computer closet near the elevator.\nIt runs on a Raspberry Pi that is located behind the network switching cabinet.\nIt automatically reboots each morning at 02:00AM and sends this message at 02:15AM.\nIf a message is not received at 02:15AM the Controller may be down and may need to be rebooted.\nThe code for the controller can be found at https://github.com/joelklammer/AQI_Controller\n\nYou can access the device from a command prompt using ssh pi@%s' % (ipaddr_a)

# Creates the text, subject, 'from', and 'to' of the message.
msg = MIMEText(my_ip_a + "\n" + my_ip_b)
msg['Subject'] = 'IP for the AQI Controller on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
# Sends the message
smtpserver.sendmail(gmail_user, [to], msg.as_string())
# Closes the smtp server.
smtpserver.quit()
