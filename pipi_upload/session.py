#@reboot python3 /home/pi/RFID/client_pLCD_displayokus_RFID.py
#sudo killall python3


from datetime import datetime
import time
import RPi.GPIO as GPIO
from lcd_display import display
import web_requests
import config
import button
from log import write_log


def user_check ():

    display ("User check","","" ,"") 
    web_requests.crm_request_user_by_rfid()
    
   
    
def reservation_check ():

    display ("Reservation check","","" ,"",True, True, sleep=2) 

    if config.in_crm == True:
        status_code = web_requests.booking_request_start_recording()
        print ("Status code from booking: " + str(status_code))  
        
        if config.logged_in == False:
        # Display error notifications, when booking error occures
            if status_code == 400:
                LCD_display.booking_400 ()
            elif status_code == 404:
                LCD_display.booking_404 ()
            elif status_code == 500:
                LCD_display.booking_500 ()  
            
        #User has reservation on the machine in appropriate time window
        else:   
        #after succesfull login display will show ("you are logged in as _user name_")
            if status_code == 200:
                #LCD_display.booking_200 ()
                print ("Recording started")
                LCD_display.booking_409_init ()
            elif status_code == 409:
                LCD_display.booking_409_init ()
            print("Recording ID: " + str(config.recording_id))
            print("Reservation ID: " + str(config.reservation_id))
    else:
        

def session_recording (refresh_rate = 5):
    
    if config.in_crm == True and config.logged_in == True:
        
          
        button.ending_reservation() #start the script which will monitor "STOP SESSION" button
        print ("Recording is running")
        
        #Loop checking and updating session information - remaining time, number of files
        while config.remaining_time > 0 :
            web_requests.checkToken()
            #print ("check token in while loop")
            time.sleep (refresh_rate) #refresh rate of remaining time and files in seconds
            if config.ended_by_user == True: 
                break  
            
            #print ("session loop")
            web_requests.booking_request_files ()
            web_requests.booking_reservation_info ()
            LCD_display.booking_409_recording ()          
     
            #print ("Status code from booking during session: " + str(config.status_code))  
            if (0 < config.remaining_time < 6) and config.warning_sent == False:
                # Session about to end warning at 5-minute mark 
                config.warning_sent = True
                LCD_display.about_to_end_w ()  
        else :
            web_requests.booking_stop_reservation ()
            write_log(11, datetime.now(), "Ended by time")
        
  
def session_end ():
    if config.logged_in == True:
        print ("Ending session")
        config.in_session = False
       
        #when session is ended by time out, or by pressing the button    
        try:
            button.button_deactivated ()
            time.sleep (1)
        except Exception as button_e:
            print (button_e)
            
        
        LCD_display.session_ended()        
        time.sleep (3)
                    
        print ("Clearing states")     
        config.ended_by_user = False   
        
        config.warning_sent = False
        config.logged_in = False
        # GPIO.cleanup(config.button_pin) # it is necessary to figure out how the button pin reacts on cleaning
        print ("Recording ended")     
        time.sleep(1)

