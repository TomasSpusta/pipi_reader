#@reboot python3 /home/pi/RFID/client_pokus_RFID.py
#sudo killall python3


import time
import RPi.GPIO as GPIO
import LCD_display
import web_requests
import config

i=0
    

def main_script():
    #get id card from rfid reader           
    web_requests.rfid_reader()
    #get response from CRM server => user name, user ID or not in database
    web_requests.crm_request_rfid()
    
    if config.in_database == False:
        LCD_display.not_in_database()
    else:
        status_code = web_requests.booking_request_start_measurement()
        print (type (status_code))
        print ("Status code from booking: " + str(status_code))  
         
        if config.logged_in == False:
            if status_code == 400:
                LCD_display.booking_400 ()
            elif status_code == 404:
                print (status_code)
                LCD_display.booking_404 ()
            elif status_code == 500:
                LCD_display.booking_500 ()
            
        #initial screen si waiting screen ("Welcome on _instrument name_, please log in with ID card")
        
        else:
        #after succesfull login display will show ("you are logged in as _user name_")
            if status_code == 200:
                LCD_display.booking_200 ()
            elif status_code == 409:
                LCD_display.booking_409 ()
                       
            #LCD_display.LCD_logged_in ()
    time.sleep(1)

    
    
    
def measuring ():
    if config.status_code == 409:
        
        print (i+1)
        LCD_display.booking_409 ()
        time.sleep (5)
        web_requests.booking_request_start_measurement()
        web_requests.booking_request_files ()
    else:
        pass     
        
    
    
    
    
    

# running script
try:
    LCD_display.LCD_waiting()
    while 1:
        main_script()
        measuring()

finally:
    time.sleep(0.5)
    LCD_display.backlight (False)
    LCD_display.clear ()        
    GPIO.cleanup()
# 