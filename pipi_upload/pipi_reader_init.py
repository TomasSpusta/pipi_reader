# This script will run as the first script - initialization, on RPi start-up
#1: Need to check internet connection => 
    #Display IP adress, 
    #if not connected, display "Not connected"
#2: Check and display the Mac adress of the RPi
#3: download new firmware
#4: Run "pipi_reader.py"

import config
from requests import get
from getmac import get_mac_address as gma #module for mac adress
import time
import LCD_display
import web_requests

pi_online_status = False
# try to acquire IP adress, therefore check connection to the internet
while pi_online_status == False:
    try:
        ip = get('https://api.ipify.org').content.decode('utf8')
        print('My public IP address is: {}'.format(ip))    
        pi_online_status = True
        
    except Exception as e: # if there is an error = no connection to net, ip = 0
        ip = 0
        print (e) 
     
    try:   
        config.mac_address = gma() # get MAC address
        print("My MAC adress is: {}".format(config.mac_address))
        
        try:
            web_requests.crm_request_mac()
        except Exception as  e2:
            print (e2)
            print ("problemek s CRM")
    except Exception as e3:
        config.mac_address = 0
        print (e3)

print (config.equipment_name, config.equipment_id)        
time.sleep (1)
LCD_display.LCD_init (ip, config.mac_address)




if ip != 0:
    time.sleep (1)    
    print ("Checking github")
    import github_repo
    
    time.sleep (1) #Sleep x seconds before it will run main script 
    print ("Main script start")
    import pipi_reader

