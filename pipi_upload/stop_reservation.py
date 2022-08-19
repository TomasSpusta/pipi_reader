import gpiozero
import time
import LCD_display

button = gpiozero.Button (21)

i = 0
session_running = True

def ending_session ():    
    button.when_pressed = loading_bar
    button.when_released = loading_bar_erase 


def loading_bar():
    symbol = "#"
    global i
    global session_running
    LCD_display.write ('Ending session',1)
    while button.is_pressed == True:
        
        #print ('Button is pressed')
        #time.sleep (0.5)
        
        i += 4
        LCD_display.write (i*symbol,2)
        print (i*symbol)
        time.sleep (1)
        if i > 16:
            print ('session ended')
            LCD_display.lcd.clear()
            LCD_display.write ('Session Ended',1)
            session_running = False # tady bude vlastne sctript, ktery odesle nekam neco, aby sa session ukoncila
            time.sleep (2)


def loading_bar_erase():
    global i
    i = 0
    LCD_display.lcd.clear()

'''
ending_session ()

t=0
while session_running == True:
    #global session_running
    t+=1
    print (t)
    time.sleep (2)
'''