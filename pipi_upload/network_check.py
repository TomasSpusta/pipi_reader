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
import time
import RPi.GPIO as GPIO
import netifaces as ni

def network_check (): 
    pi_online_status = False
    # try to acquire IP adress, therefore check connection to the internet
      
    while pi_online_status == False:
        try:
            ip_eth0 = ni.ifaddresses ("eth0")[ni.AF_INET][0]["addr"]
            
        except Exception as ip_e_eth0:
            print (ip_e_eth0)
            ip_eth0 = 0
            
        try:
            ip_wlan0 = ni.ifaddresses ("wlan0")[ni.AF_INET][0]["addr"]
        
        except Exception as ip_e_wlan0:
            print (ip_e_wlan0)
            ip_wlan0 = 0
            
        
            
            #print('My public IP address is: {}'.format(ip))    
            print('My local eth0 IP address is: {}'.format(ip_eth0))  
            print('My local wlan0 IP address is: {}'.format(ip_wlan0))  
            
       
        
        if ip_eth0 or ip_wlan0 != 0:
            
            if ip_eth0 !=0:
                ip = ip_eth0
            else:
                ip = ip_wlan0 
            
            pi_online_status = True
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
                config.mac_address = " "
                print (mac_e)
                print ("Problem with MAC address")
        else:
            LCD_display.LCD_init (ip, config.mac_address)
            time.sleep (1)
            

    print ("Equipment name: " + str (config.equipment_name))
    print ("Equipment ID: " + str (config.equipment_id))
            
    LCD_display.LCD_init (ip, config.mac_address)




    
