from datetime import datetime
#import RPi.GPIO as GPIO
import RPi as GPIO
import time
from lcd_display import display, backlight
import glob_vars
from web_requests import booking_stop_recording
from log import write_log


#Setup a GPIO pin on RPi
GPIO.setup(glob_vars.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def end_reservation ():
    #Function dealing with exding the reseravation after button is pushed for 2 seconds
    print ("Button activated")  
    GPIO.add_event_detect(glob_vars.button_pin, GPIO.BOTH, callback = button_callback, bouncetime = 50)
    
    
def button_deactivated ():
    #Deactivate button, so it cannot be pressed outside the running session
    GPIO.remove_event_detect(glob_vars.button_pin)
    print("button deactivated")
    
def button_callback (button_pin):
    #Function dealing with putton press
    i = 0    
    if GPIO.input (button_pin) == GPIO.HIGH:
        print("Button released")
        i = 0   
        backlight (False)
       
    else:
        print("Button Pressed")
             
        while GPIO.input (button_pin) == GPIO.LOW:
            backlight(True)
            i += 1

            button_hold_time = 1.5 #hold time in seconds
            time.sleep (button_hold_time/18)
            if i > 19:
               
                display ('Session ended','by user',"","", clear=True, backlight_status=True)
                                                     
                booking_stop_recording()
                write_log(11, datetime.now(), "Ended by user")
                glob_vars.ended_by_user = True
                time.sleep (2)

                
