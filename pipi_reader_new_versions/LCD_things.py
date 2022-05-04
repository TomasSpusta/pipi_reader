import time
from rpi_lcd import LCD

lcd = LCD()

def LCD_waiting (instrument_name):
    #global logged_in
    #logged_in = False
    lcd.clear() #clear the display
    lcd.text("Welcome on " + instrument_name, 1)  #print/show string on line 2
    #lcd.text(instrument_name, 2) #print/show string on line 3
    lcd.text("Please log in with your user card",3)
    
def LCD_init (ip, mac):
    lcd.clear() #clear the display
    lcd.text("IP adress:" , 1)  #show IP adress
    if ip == 0: #if there is not internet connection, therefore IP is 0
        lcd.text("Not Connected", 2)     #show not connected
    else:
        lcd.text(ip, 2) # otherwise display IP adress
    lcd.text("MAC adress",3) # display MAC adress
    lcd.text(mac,4)
    
