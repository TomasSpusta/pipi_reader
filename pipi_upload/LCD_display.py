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
def flashing (interval, number):
    for _ in range (number):
        time.sleep (interval)
        lcd.backlight (True)
        time.sleep(interval)
        lcd.backlight (False)
        
def clear():
    lcd.clear()

def write (text, row):
    lcd.cursor_pos = (row-1, 0)
    lcd.write_string (text)

def backlight (status=True):
    lcd.backlight_enabled = status

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

def LCD_logged_in (): # function dealing with displaying to the LCD display
    config.logged_in = True
    #print ("LCD_section")
    
    if config.in_database == False:
        #print ("Card is not in database")
        lcd.clear() #clear the display
        write("Card is not in a database" , 1)  #print/show string on line 1
        write("Please contact User office" , 3)
        
        time.sleep(5)
        #print (logged_in)
        LCD_waiting()
        """    
    elif server_response == "Server Error":
        #print ("Server error")
        lcd.clear() #clear the display
        write("Server Error" , 1)
        config.logged_in = False
        time.sleep(5)
        LCD_waiting(instrument_name)
        """    
    if config.in_database == True:
        config.logged_in = True
        lcd.clear() #clear the display
        write ("You are logged as:" , 1)  #print/show string on line 1
        write (str(config.user_name), 2) 
        write ("Happy hunting", 3)
        #lcd.text("Your session ends at:" , 3)  
        #lcd.text ("-end time-", 4)
        time.sleep(5)
        backlight (False)



def about_to_end_w (remaining_time): ### Dodelat, aby ukazoval session is about to end a blikalo
    lcd.clear() #clear the display
    write ("Dear user,\n\ryour session\n\ris about to end\n\rin " + str(remaining_time) + (" minutes"), 1)
    flashing(0.3, 5) 
    backlight(True)
    time.sleep (3)
    backlight (False)

def session_expired_w (): # chceme nejake auto odhlasenie po expiracii?
    lcd.clear()
    write ("Dear user,\n\ryour session\n\rhas expired", 1)
    #lcd.text ("Dear user, your session expired, you will be automaticly logged off in 5 minutes", 1)
    backlight(True)




    
