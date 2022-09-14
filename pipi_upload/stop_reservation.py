import RPi.GPIO as GPIO
import time
import LCD_display
import config
import web_requests


GPIO.setup(config.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
i = 0

def ending_reservation ():    
    GPIO.add_event_detect(config.button_pin, GPIO.BOTH, callback = button_callback, bouncetime = 50)

def button_deactivated ():
    GPIO.remove_event_detect(config.button_pin)
    
def button_callback (button_pin):    
    if GPIO.input (button_pin) == GPIO.HIGH:
        i = 0
        LCD_display.clear()
        LCD_display.booking_409_time ()
        
    else:
        symbol = "|"
        LCD_display.backlight(True)
        LCD_display.clear()
        LCD_display.write ('Ending session',1)
        
        while GPIO.input (button_pin) == GPIO.LOW:
            i += 1
            LCD_display.write (i*symbol,2)
            button_hold_time = 2 #hold time in seconds
            time.sleep (button_hold_time/18)
            if i > 19:
                GPIO.remove_event_detect(button_pin)
                web_requests.booking_stop_reservation()
                LCD_display.clear()
                LCD_display.write ('Session ended',1)
                LCD_display.write ('by user',2)             
                time.sleep (5)
                
