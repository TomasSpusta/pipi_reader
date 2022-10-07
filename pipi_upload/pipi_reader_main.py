# Main Pipi reader file
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


#Import section
import faulthandler
import RPi.GPIO as GPIO
import time


from network_check import network_check
from github_check import github_check

try:
    faulthandler.enable ()
    #Check internet connection, acquire IP address and MAC address
    network_check ()
    time.sleep (3)

    #Connect to GIT HUB and download the latest version from "main" or "develop" branch
    github_check (branch = "develop_reconstruction")
    time.sleep (5)
    
    from card_reader import card_reader
    import session
    import LCD_display
    
    
    time.sleep (3)
    
    session_recording_thread = threading.Thread (target=session.session_recording, daemon=True)

    while 1:
        try:
            #initial waiting screen
            LCD_display.LCD_waiting()
            
            #Wait for the card swipe 
            card_reader ()
            
            #check if user is in the RFID database
            session.user_check ()
            
            #check if the user has reservation on the equipment
            #in appropriate time window and start recording
            session.reservation_check ()
            
            #every X seconds check the remaining time of session and number of acquired files
            session.session_recording ()
            
            # when session ends reset variables for new user
            session.session_end ()
        
        except Exception as e:
            print("Error in main code")
            print(e)   

except KeyboardInterrupt:
    print("CTRL + V pressed, script ended in pipi_reader script")
    
    time.sleep (0.5)
    LCD_display.backlight (False)
    LCD_display.clear ()        
    GPIO.cleanup ()
    
