# This script will run as the first script - initialization, on RPi start-up
#1: Need to check internet connection => 
    #Display IP adress, 
    #if not connected, display "Not connected"
#2: Check and display the Mac adress of the RPi
#3: download new firmware
#4: Run "pipi_reader.py"

import datetime
import config
from requests import get
from getmac import get_mac_address as gma #module for mac adress
import LCD_display
import web_requests
import time
import RPi.GPIO as GPIO
import netifaces as ni
from log import write_log, open_sh


def network_check (): 
    config.online_status = False
    # try to acquire IP adress, therefore check connection to the internet
      
    while config.online_status == False:
        LCD_display.display ("Network check","","" ,"",True, True, sleep=2) 
        
        try:
            ip_eth0 = ni.ifaddresses ("eth0")[ni.AF_INET][0]["addr"]         
        except Exception as ip_e_eth0:
            print (ip_e_eth0)
            
            ip_eth0 = 0
        #print('My local eth0 IP address is: {}'.format(ip_eth0))     
        
        try:
            ip_wlan0 = ni.ifaddresses ("wlan0")[ni.AF_INET][0]["addr"]       
        except Exception as ip_e_wlan0:
            print (ip_e_wlan0)
            
            ip_wlan0 = 0
        #print('My local wlan0 IP address is: {}'.format(ip_wlan0))
       
        
        if ip_eth0 or ip_wlan0 != 0:
            
            if ip_eth0 !=0:
                config.ip_eth0 = ip_eth0
               
                
            if ip_wlan0 !=0:
                config.ip_wlan0 = ip_wlan0
                
                
            if ip_eth0 !=0:
                ip = ip_eth0
            else:
                ip = ip_wlan0
            
            config.online_status = True
            
            try:
                open_sh(config.mac_address)
                write_log(1,datetime.now())
                write_log(2,config.ip_eth0,datetime.now())
                write_log(3,config.ip_wlan0,datetime.now())
            except Exception as sh_log_error:
                print ("sh_log_error: " + str(sh_log_error))
                LCD_display.display ("Log sh error", sh_log_error,"" ,"",clear=True, backlight_status=True,sleep=2) 
            
            try:   
                config.mac_address = gma() # get MAC address
                print("My MAC adress is: {}".format(config.mac_address))
                
                # Send request to CRM to obtain equipment info according to MAC address
                web_requests.crm_request_mac()
               
                    
            except Exception as mac_e:
               
                print (mac_e)
                print ("Problem with MAC address")
        else:
            LCD_display.LCD_init (ip, config.mac_address)
            time.sleep (3)        

    print ("Equipment name: " + str (config.equipment_name))
    print ("Equipment ID: " + str (config.equipment_id))
       
    LCD_display.LCD_init (ip, config.mac_address)





    
