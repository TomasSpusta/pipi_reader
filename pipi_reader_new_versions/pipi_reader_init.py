# This script will run as the first script - initialization, on RPi start-up
#1: Need to check internet connection => 
    #Display IP adress, 
    #if not connected, display "Not connected"
#2: Check and display the Mac adress of the RPi
#3: download new firmware
#4: Run "pipi_reader_main.py"


from requests import get
from getmac import get_mac_address as gma #module for mac adress
import time
import LCD_things

online = False
# try to acquire IP adress, therefore check connection to the internet
while online == False:
    try:
        ip = get('https://api.ipify.org').content.decode('utf8')
        print('My public IP address is: {}'.format(ip))    
        online = True
    except Exception as e: # if there is an error = no connection to net, ip = 0
        ip = 0
        #print (e) 
     
    try:    
        mac = gma() # get MAC address
        print("My MAC adress is: {}".format(mac))
    except Exception as e2:
        mac = 0
        print (e2)
        
     
    time.sleep (1)
    LCD_things.LCD_init (ip, mac)



if ip != 0:
    time.sleep (5)
    import check_github_repo
    time.sleep (5) #Sleep x seconds before it will run main script 
    import PiPi_reader

