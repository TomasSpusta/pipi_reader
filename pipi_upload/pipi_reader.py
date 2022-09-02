#@reboot python3 /home/pi/RFID/client_pokus_RFID.py
#sudo killall python3


import time
import RPi.GPIO as GPIO
import LCD_display
import web_requests
import config
import card_reader
import stop_reservation
import logs    

def main_script():
    
   
    #get card id from rfid reader           
    card_reader.rfid_reader()
    #get response from CRM server => user name, user ID or not in database
    web_requests.crm_request_rfid()


    if config.in_database == False:
        # If card ID is not it the internal database, LCD displays the error 
        LCD_display.not_in_database() 
    else:
        # Load the status code of reservation
        config.status_code = web_requests.booking_request_start_measurement()
        #print (type (status_code))
        #print ("Status code from booking: " + str(config.status_code))  
         
        if config.logged_in == False:
            # Display error notifications, when booking error occures
            if config.status_code == 400:
                LCD_display.booking_400 ()
            elif config.status_code == 404:
                LCD_display.booking_404 ()
            elif config.status_code == 500:
                LCD_display.booking_500 ()  
              
        else:
            stop_reservation.ending_reservation() #start the script which will monitor "STOP SESSION" button
        #after succesfull login display will show ("you are logged in as _user name_")
            if config.status_code == 200:
                LCD_display.booking_200 ()
                print ("Recording started")
                LCD_display.booking_409_init ()
            elif config.status_code == 409:
                LCD_display.booking_409_init ()
            print("Recording ID: " + str(config.recording_id))
            print("Reservation ID: " + str(config.reservation_id))
           
            logs.start()
            
            refresh_rate = 10 #refresh rate of remaining time and files in seconds    
            while config.remaining_time > 0 :
                #Loop checking and updating session information - remaining time, number of files
                #config.status_code = web_requests.booking_request_start_measurement()
                web_requests.booking_request_files()
                web_requests.booking_reservation_info ()
                time.sleep (refresh_rate) # refresh rate in seconds   
                LCD_display.booking_409_time ()
                print ("Recording is running")
                #print ("Status code from booking during session: " + str(config.status_code))  
                if (0 < config.remaining_time < 6) and config.warning_sent == False:
                    # Session about to end warning at 5-minute mark 
                    config.warning_sent = True
                    LCD_display.about_to_end_w ()
                   
                #elif config.in_session == True and #(config.status_code == 404 or config.status_code == 500) :
                    #This should check when the session is terminated manualy in the booking system
                    #LCD_display.session_ended () 
                #    config.remaining_time = 0       
                
            
            LCD_display.session_ended ()
              
            config.in_session = False
            config.warning_sent = False
            config.logged_in = False
            print ("Recording ended")     
           
    time.sleep(1)


    

# running script

try:
    LCD_display.LCD_waiting()
    while 1:
        main_script()
    
    
except KeyboardInterrupt:
    print("CTRL + V pressed, script ended in pipi_reader script")
    
    time.sleep(0.5)
    LCD_display.backlight (False)
    LCD_display.clear ()        
    GPIO.cleanup()

    
# 