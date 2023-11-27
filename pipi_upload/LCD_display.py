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

def backlight (status=True):
    lcd.backlight_enabled = status

    
def flashing (interval, number):
    for _ in range (number):
        time.sleep (interval)
        lcd.backlight_enabled = True
        time.sleep(interval)
        lcd.backlight_enabled = False
        
def display (line1, line2, line3, line4, clear = True, backlight_status = True, sleep = 0):
    # display ("Your VUT card is not", "in database yet.", "Let's change that.","", clear = True)
    lcd.backlight_enabled = backlight_status
    if clear == True:
        lcd.clear()
    write (line1,1)
    write (line2,2)
    write (line3,3)
    write (line4,4)
    time.sleep (sleep)
        
def clear():
    lcd.clear()

def write (text, row):
    lcd.cursor_pos = (row-1, 0)
    lcd.write_string (text)

def version ():
    display ("","Version:",config.git_release,"",clear=True, backlight_status=True)

def LCD_init (ip, mac):
    lcd.backlight_enabled = True
    lcd.clear() #clear the display
    write ("IP adress:", 1) #show IP adress
    
    if ip == 0: #if there is not internet connection, therefore IP is 0
        write ("Not Connected", 2)     #show not connected
    else:
        write (ip, 2) # otherwise display IP adress
    write ("MAC adress:",3) # display MAC adress
    write (mac,4)
    
def LCD_waiting ():
    config.logged_in = False
    display ("Welcome on ", config.equipment_name,"Please log in", "with your user card" ,clear=True, backlight_status=True) 
    

def not_in_database ():
    #user card is not in internal database, need to contact user office
    display ("Your card","is not in database.","Please register it","in booking system.",clear=True, backlight_status=True)
    time.sleep (5)
    LCD_waiting()
    
def booking_200 ():
    display ("Hi",config.user_name,"Recording started","Happy hunting!",clear=True, backlight_status=True)
    #time.sleep(5)
    

def booking_409_init ():
    display ("Recording is running", "To stop it", "hold the red button","for 3 seconds", clear=True, backlight_status=True)
    #time.sleep (5)
    #lcd.clear()
    

def booking_409_recording (): 
    display("Remaining time:", str(config.remaining_time) + " min", "Number of files:", str(config.files) + " files", clear=True, backlight_status=False)
    

def booking_400 ():
    display ("Hi",str(config.user_name),"Invalid booking","parameters.",clear=True,backlight_status=True)
    time.sleep (5)
    LCD_waiting()

def booking_404 ():
    #display ("Hi",str(config.user_name),"No future bookings.","Please make one.",clear=True,backlight_status=True)
    #display("No future bookings", "of yours", "in next 30 minutes.", "Please make one.", clear=True, backlight_status=True)
    display("You have any", "future bookings", "in next 30 minutes.", "Please make one.", clear=True, backlight_status=True)
    time.sleep (5)
    LCD_waiting() 
    
def booking_500 ():
    display ("Hi",str(config.user_name),"Internal ERROR.","Try to log in again.",clear=True,backlight_status=True)
    time.sleep (5)
    LCD_waiting()
    
def in_database ():
    #user card is in internal database
    display ("Hi",str(config.user_name),"Recording started.","Happy hunting!",clear=True,backlight_status=True)   

def about_to_end_w (): ### Dodelat, aby ukazoval session is about to end a blikalo
    display (str(config.user_name),"Your session","is about to end","in " + str(config.remaining_time) + " minutes.", clear=True,backlight_status=True)
    flashing(0.3, 5) 
    time.sleep (5)

def session_ended ():
    display ("Hi",str(config.user_name),"Your session ended.","See you next time.",clear=True,backlight_status=True)  