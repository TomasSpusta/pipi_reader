#@reboot python3 /home/pi/RFID/client_pokus_RFID.py
#sudo killall python3


import time
import RPi.GPIO as GPIO
import LCD_display
import web_requests
import config

def main_script():
    #get id card from rfid reader           
    config.card_id = web_requests.rfid_reader()
    #print ('RFID number from reader: ' + str(rfid_number))
    #get response from server => user name, or not in database
    crm_response_rfid = web_requests.crm_request_rfid(config.card_id)
    
    if config.in_database == False:
            #initial screen si waiting screen ("Welcome on _instrument name_, please log in with ID card")
        LCD_display.LCD_waiting(config.equipment_name)
    else:
        #after succesfull login display will show ("you are logged in as _user name_")
        LCD_display.LCD_logged_in (config.user_name)
    time.sleep(1)
    
    
    

# running script
try:
    LCD_display.LCD_waiting(config.equipment_name)
    while 1:
        main_script()

finally:
    time.sleep(0.5)
    LCD_display.backlight (False)
    LCD_display.clear ()        
    GPIO.cleanup()
# 