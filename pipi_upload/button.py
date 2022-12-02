import RPi.GPIO as GPIO
import time
import LCD_display
import config
from web_requests import booking_stop_reservation



GPIO.setup(config.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def ending_reservation ():
    ("ending reservation")  
    GPIO.add_event_detect(config.button_pin, GPIO.BOTH, callback = button_callback, bouncetime = 50)
    
    
def button_deactivated ():
    GPIO.remove_event_detect(config.button_pin)
    print("button deactivated")
    
def button_callback (button_pin):
    i = 0    
    if GPIO.input (button_pin) == GPIO.HIGH:
        print("Button released")
        i = 0   
        LCD_display.backlight (False)

        
    else:

        print("Button Pressed")
        
      
        while GPIO.input (button_pin) == GPIO.LOW:
            LCD_display.backlight(True)
            i += 1
            #LCD_display.write (i*symbol,2)
            button_hold_time = 1.5 #hold time in seconds
            time.sleep (button_hold_time/18)
            if i > 19:
                button_deactivated ()
                booking_stop_reservation()
                LCD_display.display ('Session ended','by user',"","",clear=True,backlight_status=True)
                config.ended_by_user = True             
                time.sleep (2)
                #LCD_display.session_ended ()
                
