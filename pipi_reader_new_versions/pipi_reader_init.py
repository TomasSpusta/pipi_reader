# This script will run as the first script - initialization, on RPi start-up
#1: Need to check internet connection => 
    #Display IP adress, 
    #if not connected, display "Not connected"
#2: Check and display the Mac adress of the RPi
#3: Run "pipi_reader_main.py"

from rpi_lcd import LCD # module for LCD dispaly 
from requests import get
from getmac import get_mac_address as gma #module for mac adress
import time
import test_file
import LCD_things

#create LCD dispaly instance
#lcd = LCD() 

# try to acquire IP adress, therefore check connection to the internet
try:
    ip = get('https://api.ipify.org').content.decode('utf8')    
except Exception as e: # if there is an error = no connection to net, ip = 0
    ip = 0
    print (e) 
    
mac = gma() # get MAC address

print('My public IP address is: {}'.format(ip))
print("My MAC adress is: {}".format(mac))

LCD_things.LCD_init (ip, mac)


time.sleep (5) #Sleep 10 seconds before it will run main script 

import PiPi_reader

