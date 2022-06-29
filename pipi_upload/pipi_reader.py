#@reboot python3 /home/pi/RFID/client_pokus_RFID.py
#sudo killall python3


import time
import RPi.GPIO as GPIO
import LCD_display
import web_requests
import config

    

def main_script():
    i=0
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
                print ("measuring module started")
                i = i + 1
                print (i)
                LCD_display.booking_409 ()
                time.sleep (5)
                web_requests.booking_request_start_measurement()
                web_requests.booking_request_files ()
                       
            #LCD_display.LCD_logged_in ()
    time.sleep(1)

    
    
"""   
def measuring ():
    print ("measuring module started")
    if config.status_code == 409:
        i= i +1
        print (i)
        LCD_display.booking_409 ()
        time.sleep (5)
        web_requests.booking_request_start_measurement()
        web_requests.booking_request_files ()
    else:
        pass     
"""        
    
    
    
    
    

# running script
try:
    LCD_display.LCD_waiting()
    while 1:
        main_script()
      
finally:
    time.sleep(0.5)
    LCD_display.backlight (False)
    LCD_display.clear ()        
    GPIO.cleanup()
# 