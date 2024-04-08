from datetime import datetime
import time
from lcd_display import display, backlight
import glob_vars
from web_requests import booking_stop_recording
from log import write_log

'''
def activate_button ():
    
    button = Button(21)    
    if button.closed == True:
        print ("Btn was closed, creating new button")
        button = Button(21)
    else:
        print ("Btn is open")
    return button
'''

def end_reservation (button):
    #Function dealing with exding the reseravation after button is pushed for 2 seconds
    print ("Button activated")  
    button.hold_time = 1.5
    button.when_held = button_callback
    #GPIO.add_event_detect(glob_vars.button_pin, GPIO.BOTH, callback = button_callback, bouncetime = 50)
    
def button_deactivated (button):
    #Deactivate button, so it cannot be pressed outside the running session
    #button.active_state = False
    button.close ()
    #GPIO.remove_event_detect(glob_vars.button_pin)
    print("button deactivated")
    
def button_callback ():
    #Function dealing with putton press
    display ('Session ended','by user',"","", clear=True, backlight_status=True)
    booking_stop_recording()
    write_log(11, datetime.now(), "Ended by user")
    glob_vars.ended_by_user = True
    time.sleep (2)
