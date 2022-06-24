#@reboot python3 /home/pi/RFID/client_pokus_RFID.py
#sudo killall python3


import time
import RPi.GPIO as GPIO
import LCD_display
import web_requests
import config

instrument_name = config.instrument_name 
#in the future instrument name will be pulled from online database (google sheets are complicated) 
#probably some database in the booking system web?

#initial user status is logged off
config.logged_in = False


def main_script():
    #get id card from rfid reader           
    config.card_id = web_requests.RFID_reader()
    #print ('RFID number from reader: ' + str(rfid_number))
    #get response from server => user name, or not in database
    crm_response = web_requests.crm_request()
    server_response = web_requests.send_receive_data(rfid_number)
    #print (server_response)
    
    if config.logged_in == False:
        #initial screen si waiting screen ("Welcome on _instrument name_, please log in with ID card")
        LCD_display.LCD_waiting(instrument_name)
    else:
        #after succesfull login display will show ("you are logged in as _user name_")
        LCD_display.LCD_logged_in (server_response, instrument_name)
    time.sleep(1)

# running script
try:
    LCD_display.LCD_waiting(instrument_name)
    while 1:
        main_script()

finally:
    time.sleep(0.5)
    LCD_display.backlight (False)
    LCD_display.clear ()        
    GPIO.cleanup()
# 