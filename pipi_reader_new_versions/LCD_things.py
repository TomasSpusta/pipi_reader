import time
from rpi_lcd import LCD

lcd = LCD()

def LCD_waiting (instrument_name):
    #global logged_in
    #logged_in = False
    lcd.clear() #clear the display
    lcd.text("Welcome on" , 1)  #print/show string on line 2
    lcd.text(instrument_name, 2) #print/show string on line 3
    lcd.text("Please log in with your user card",3)
    
def LCD_init ():
    print()
    
