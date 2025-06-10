'''
1. Check internet connection, obtain IP and MAC address => internet module
2. Check and obtain equipment_id and equipment_name from CRM via MAC address
3. Wait till card is obtained - card_id
4. Check if user (card_id) is in CRM database, if yes obtain user_id, user_name etc. 
    if use is not in database, show message to visit user office
5. With user_id and equipment_id check reservation
    depending on response from booking system start recording
        - obtain reservation_id an recording_id
    or display error message (400, 404, 500)
6. Every X (5 now) seconds check remaining_time of reservation (and files acquirec)
7. If remaining_time is near end of reservation show message about the end
8. If button is pressed, end recording (send reservation?_id and equipment_id) 

'''

import datetime as dt
import glob_vars
#import RPi.GPIO as GPIO
import time
from lcd_display import display, waiting, backlight, clear
from log import write_log
from rfid_reader import card_reader
import session
import web_requests
from gpiozero import Button

def main ():
    try:
        web_requests.load_token_data()
        display ("Main starting","","" ,"") 
        write_log(6, dt.datetime.now())
        time.sleep (1)
        button = Button(glob_vars.button_pin)
        
        while True:
            try:
                if button.closed == True:
                    print("Button closed, creating button")
                    button = Button(glob_vars.button_pin)
                else:
                    print("Button open")
                    pass
                #initial waiting screen
                waiting ()
                
                #Wait for the card swipe 
                card_reader ()
                display("Card Scanned","","","")
                
                #check if user is in the CRM database
                web_requests.crm_request_user_by_rfid()
                #session.user_check ()
                        
                #check if the user has reservation on the equipment
                #in appropriate time window and start recording
                
                session.start_recording ()
                
                #every X seconds check the remaining time of session and number of acquired files
                session.session_recording (button, refresh_rate= 5)
                        
                # when session ends reset variables for new user
                session.session_end (button)
                
            
            except Exception as main_loop_e:
                print("Error in main while code: " + str(main_loop_e))
                display("Main while error", str(main_loop_e),"","",True,True,2)

    except Exception as main_code_e:
        print("Error in main code: " + str(main_code_e))
        display("Main code error", str(main_code_e), "", "", True,True,2)

    except KeyboardInterrupt:
        print("CTRL + V pressed, script ended in pipi_reader script")
        time.sleep (0.5)
        backlight (False)
        clear ()        
        #GPIO.cleanup ()
    