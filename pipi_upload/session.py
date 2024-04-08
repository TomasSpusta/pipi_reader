#@reboot python3 /home/pi/RFID/client_pLCD_displayokus_RFID.py
#sudo killall python3


from datetime import datetime
import time
#import RPi.GPIO as GPIO
#import gpiozero
from lcd_display import display, waiting, flashing
import web_requests
import glob_vars
import button_gpiozero
from log import write_log
    
def start_recording ():

    display ("Reservation check","","" ,"",True, True, sleep=2) 

    if glob_vars.in_crm == True:
        status_code = web_requests.booking_request_start_recording()
        print ("Status code from booking: " + str(status_code))  
        
        if glob_vars.recording_started == False:
        # Display error notifications, when booking error occures
            if status_code == 400:
                display ("Hi",str(glob_vars.user_name),"Invalid booking","parameters.",True,True,5)
            elif status_code == 404:
                display("You have no", "future bookings", "in next 30 minutes.", "Please make one.", True, True,5)
            elif status_code == 500:
                display ("Hi",str(glob_vars.user_name),"Internal ERROR.","Try to log in again.",True,True,5)
        #waiting() !!! uvidime jak to bude fungovat bez tohoto
            
        #User has reservation on the machine in appropriate time window
        else:   
        #after succesfull login display will show ("you are logged in as _user name_")
            display ("Hi",glob_vars.user_name,"Recording started"," or is running",True, True, 2)
            display ("To stop it", "hold the button","for 3 seconds","", True, True,2)
            
            '''
            if status_code == 200:
                #LCD_display.booking_200 ()
                print ("Recording started")
                LCD_display.booking_409_init ()
            elif status_code == 409:
                LCD_display.booking_409_init ()'''
            print("Recording ID: " + str(glob_vars.recording_id))
            print("Reservation ID: " + str(glob_vars.reservation_id))
    
        

def session_recording (refresh_rate = 5):
    
    if glob_vars.in_crm == True and glob_vars.recording_started == True:
        
          
        button_gpiozero.end_reservation() #start the script which will monitor "STOP SESSION" button
        print ("Recording is running")
        
        #Loop checking and updating session information - remaining time, number of files
        while glob_vars.remaining_time > 0 :
            web_requests.check_token()
            #print ("check token in while loop")
            time.sleep (refresh_rate) #refresh rate of remaining time and files in seconds
            if glob_vars.ended_by_user == True: 
                break  
            
            #print ("session loop")
            #web_requests.booking_request_files ()
            web_requests.booking_reservation_info ()
            display("Remaining time:", str(glob_vars.remaining_time) + " min", "","", clear=True, backlight_status=False)         
            #display("Remaining time:", str(glob_vars.remaining_time) + " min", "Number of files:", str(glob_vars.files) + " files", clear=True, backlight_status=False)         
     
            #print ("Status code from booking during session: " + str(config.status_code))  
            if (0 < glob_vars.remaining_time < 6) and glob_vars.warning_sent == False:
                # Session about to end warning at 5-minute mark 
                glob_vars.warning_sent = True
                display (str(glob_vars.user_name),"Your session","is about to end","in " + str(glob_vars.remaining_time) + " minutes.", clear=True,backlight_status=True)
                flashing(0.3, 5) 
                #display("Remaining time:", str(glob_vars.remaining_time) + " min", "Number of files:", str(glob_vars.files) + " files", clear=True, backlight_status=False)
        else :
            web_requests.booking_stop_recording ()
            
        
  
def session_end ():
    if glob_vars.recording_started == True:
        print ("Ending session")
        glob_vars.in_session = False
       
        #when session is ended by time out, or by pressing the button    
        try:
            button_gpiozero.button_deactivated ()
            time.sleep (1)
        except Exception as button_deactivation_e:
            print (button_deactivation_e)
            
        
        display ("Hi",str(glob_vars.user_name),"Your session ended.","See you next time.",True,True,3)
                    
        print ("Clearing states")     
        glob_vars.ended_by_user = False          
        glob_vars.warning_sent = False
        glob_vars.recording_started = False
        # GPIO.cleanup(config.button_pin) # it is necessary to figure out how the button pin reacts on cleaning
        print ("Recording ended")     
        time.sleep(1)

