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
from PiPi_reader import main_script


def LCD_disp(ip, mac):
    lcd = LCD() #create LCD dispaly instance
    lcd.clear() #clear the display
    lcd.text("IP adress:" , 1)  #show IP adress
    if ip == 0: #if there is not internet connection, therefore IP is 0
        lcd.text("Not Connected", 2)     #show not connected
    else:
        lcd.text(ip, 2) # otherwise display IP adress
    lcd.text("MAC adress",3) # display MAC adress
    lcd.text(mac,4)

# try to acquire IP adress, therefore check connection to the internet
try:
    ip = get('https://api.ipify.org').content.decode('utf8')    
except Exception as e: # if there is an error = no connection to net, ip = 0
    ip = 0
    print (e) 
    
mac = gma() # get MAC address
print('My public IP address is: {}'.format(ip))
print("My MAC adress is: {}".format(mac))

LCD_disp (ip, mac)

time.sleep (10) #Sleep 10 seconds before it will run main script 

main_script.PiPi_reader()

