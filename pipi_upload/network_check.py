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
import LCD_display
import web_requests
import RPi.GPIO as GPIO

def network_check (): 
    pi_online_status = False
    # try to acquire IP adress, therefore check connection to the internet
      
    while pi_online_status == False:
        try:
            ip = get('https://api.ipify.org').content.decode('utf8')
            print('My public IP address is: {}'.format(ip))    
            pi_online_status = True
            
        except Exception as ip_e: # if there is an error = no internet connection, ip = 0
            ip = 0
            print (ip_e) 
        
        if ip != 0:
            try:   
                config.mac_address = gma() # get MAC address
                print("My MAC adress is: {}".format(config.mac_address))
                
                try:
                    # Send request to CRM to obtain equipment info according to MAC address
                    web_requests.crm_request_mac()
                except Exception as  e_CRM:
                    print (e_CRM)
                    print ("CRM has problem with MAC address")
                    
            except Exception as mac_e:
                config.mac_address = 0
                print (mac_e)
                print ("Problem with MAC address")

    print ("Equipment name: " + str (config.equipment_name))
    print ("Equipment ID: " + str (config.equipment_id))
            
    LCD_display.LCD_init (ip, config.mac_address)





    
