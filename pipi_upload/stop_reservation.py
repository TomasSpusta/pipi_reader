import RPi.GPIO as GPIO
import time
import LCD_display
import config
from pipi_reader import session_check

#i = 0
session_running = True
button_pin = 40
#GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def button_callback (button_pin):    
    i=0
    #global session_running
    if GPIO.input (button_pin) == GPIO.HIGH:
        #print ('button released now')
        #session_running = True
        i = 0
        LCD_display.clear()
        LCD_display.booking_409_time ()
        
    else:
        symbol = "|"
        #print ('button Pressed now')
        LCD_display.backlight(True)
        LCD_display.clear()
        LCD_display.write ('Ending session',1)
        
        while GPIO.input (button_pin) == GPIO.LOW:
            i += 1
            LCD_display.write (i*symbol,2)
            #print (i*symbol)
            time.sleep (0.075)
            if i > 19:
                #GPIO.cleanup(button_pin)
                GPIO.remove_event_detect(button_pin)
                #print ('session ended')
                #LCD_display.clear()
                #LCD_display.write ('Session ended',1)
                #LCD_display.write ('by user',2)
                
                config.remaining_time = 0
                session_check()
                #TADY JE MISTO NA TO CO SA BUDE DIT, KED USER PODRZI TLACITKO ABY SKONCILA SESSION
                
                time.sleep (1)
                
                
def ending_reservation ():    
    GPIO.add_event_detect(button_pin, GPIO.BOTH, callback = button_callback, bouncetime = 50)

def button_deactivated ():
    GPIO.remove_event_detect(button_pin)

""""
t=0
try:
    while session_running == True:
        #global session_running
        t+=1
        print (t)
        time.sleep (1)
        
except KeyboardInterrupt:
    GPIO.cleanup()

"""
