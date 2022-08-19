import time
from RPLCD.i2c import CharLCD
import config

#initialize the LCD display, (expander chip, port)
lcd = CharLCD('PCF8574', 0x27)

#write to display:
    #lcd.write_string('Hello\r\n  World!')
    #lcd.write_string('Raspberry Pi HD44780')
    #lcd.cursor_pos = (2, 0) => (row, column)
    #lcd.write_string('https://github.com/\n\rdbrgn/RPLCD')
#Backlight control:
    #lcd.backlight_enabled = True/False
#Clear display:
    #lcd.clear()
#

def backlight (status=True):
    lcd.backlight_enabled = status
    
def flashing (interval, number):
    for _ in range (number):
        time.sleep (interval)
        backlight (True)
        time.sleep(interval)
        backlight (False)
        
def clear():
    lcd.clear()

def write (text, row):
    lcd.cursor_pos = (row-1, 0)
    lcd.write_string (text)

def version ():
    backlight (True)
    lcd.clear() #clear the display
    write ("Version:",1)
    write ("X.X.X",2)

def LCD_init (ip, mac):
    backlight (True)
    lcd.clear() #clear the display
    write ("IP adress:", 1) #show IP adress
    
    if ip == 0: #if there is not internet connection, therefore IP is 0
        write ("Not Connected", 2)     #show not connected
    else:
        write (ip, 2) # otherwise display IP adress
    write ("MAC adress:",3) # display MAC adress
    write (mac,4)
    
def LCD_waiting ():
    backlight (True)
    config.logged_in = False
    lcd.clear() #clear the display
    write ("Welcome on ", 1)  #print/show string on line 2
    write (config.equipment_name, 2) #lcd.text(instrument_name, 2) #print/show string on line 3
    write ("Please log in\n\rwith your user card", 3)

def not_in_database ():
    #user card is not in internal database, need to contact user office
    backlight (True)
    lcd.clear() #clear the display
    write ("Your card" , 1)  #print/show string on line 1
    write ("is not in a database" , 2)
    write ("Please contact", 3) 
    write ("User Office in C1.04", 4) 
    time.sleep (5)
    LCD_waiting()
    
def booking_200 ():
    backlight (True)
    lcd.clear() #clear the display
    write ("Hi", 1)  #print/show string on line 1
    write (str(config.user_name), 2)
    write ("Recording started", 3)
    write ("Happy hunting!", 4)
    time.sleep(5)
    

def booking_409_init ():
    backlight (True)
    lcd.clear() #clear the display
    write (config.user_name, 1)  #print/show string on line 1
    write ("Recording is running", 2)
    write ("To stop recording", 3)
    write ("hold the red button", 4)  
    time.sleep (5)
    

def booking_409_time (): 
    backlight (False)
    lcd.clear() #clear the display
    write ("Remaining time:", 1)  #print/show string on line 1
    #write ("   ", 2)
    write (str(config.remaining_time) + " min", 2)
    write ("Number of files:", 3)
    #write ("   ", 4)  
    write (str(config.files) + " files", 4)
    

def booking_400 ():
    backlight (True)
    lcd.clear() #clear the display
    write ("Hi", 1)  #print/show string on line 1
    write (str(config.user_name), 2)
    write ("Invalid booking", 3)
    write ("parameters", 4)
    time.sleep (5)
    LCD_waiting()

def booking_404 ():
    backlight (True)
    lcd.clear() #clear the display
    write ("Hi", 1)  #print/show string on line 1
    write (str(config.user_name), 2)
    write ("No future booking", 3)
    write ("Please make one", 4)
    time.sleep (5)
    LCD_waiting() 
    
def booking_500 ():
    backlight (True)
    lcd.clear() #clear the display
    write ("Hi", 1)  #print/show string on line 1
    write (str(config.user_name), 2)
    write ("Internal ERROR", 3)
    write ("Try to log in again", 4)
    time.sleep (5)
    LCD_waiting()

def session_ended ():
    backlight (True)
    lcd.clear() #clear the display
    write ("Hi", 1)  #print/show string on line 1
    write (str(config.user_name), 2)
    write ("Your session ended", 3)
    write ("See you next time", 4)
    time.sleep (10)
    LCD_waiting()        
    
def in_database ():
    #user card is in internal database
    backlight (True)
    lcd.clear() #clear the display
    write ("Hello", 1)  #print/show string on line 1
    write (str(config.user_name), 2)
    write ("Recording started", 3)
    write ("Happy hunting!", 4)
    

def about_to_end_w (): ### Dodelat, aby ukazoval session is about to end a blikalo
    lcd.clear() #clear the display
    write ("Dear user,\n\ryour session\n\ris about to end\n\rin " + str(config.remaining_time) + (" minutes"), 1)
    flashing(0.3, 5) 
    backlight(True)
    time.sleep (5)
    backlight (False)

def session_expired_w (): # chceme nejake auto odhlasenie po expiracii?
    lcd.clear()
    write ("Dear user,\n\ryour session\n\rhas expired", 1)
    #lcd.text ("Dear user, your session expired, you will be automaticly logged off in 5 minutes", 1)
    backlight(True)


#def ending_session ():
    

    
