import time
from rpi_lcd import LCD
import config

lcd = LCD()

def LCD_init (ip, mac):
    lcd.clear() #clear the display
    lcd.text("IP adress:" , 1)  #show IP adress
    if ip == 0: #if there is not internet connection, therefore IP is 0
        lcd.text("Not Connected", 2)     #show not connected
    else:
        lcd.text(ip, 2) # otherwise display IP adress
    lcd.text("MAC adress",3) # display MAC adress
    lcd.text(mac,4)

def LCD_waiting (instrument_name):
    
    config.logged_in = False
    lcd.clear() #clear the display
    lcd.text("Welcome on " + instrument_name, 1)  #print/show string on line 2
    #lcd.text(instrument_name, 2) #print/show string on line 3
    lcd.text("Please log in with your user card",3)
    
def LCD_logged_in (server_response, instrument_name): # function dealing with displaying to the LCD display
    #config.logged_in = True
    #print ("LCD_section")
    
    if server_response == False:
        #print ("Card is not in database")
        lcd.clear() #clear the display
        lcd.text("Card is not in a database" , 1)  #print/show string on line 1
        lcd.text("Please contact User office" , 3)
        config.logged_in = False
        time.sleep(5)
        #print (logged_in)
        LCD_waiting(instrument_name)
        
    elif server_response == "Server Error":
        #print ("Server error")
        lcd.clear() #clear the display
        lcd.text("Server Error" , 1)
        config.logged_in = False
        time.sleep(5)
        LCD_waiting(instrument_name)
        
        
    else:
        config.logged_in = True
        lcd.clear() #clear the display
        lcd.text("You are logged as:" , 1)  #print/show string on line 1
        lcd.text(str(server_response), 2) 
        lcd.text ("Happy hunting", 3)
        #lcd.text("Your session ends at:" , 3)  
        #lcd.text ("-end time-", 4)