from rpi_lcd import LCD
import time
import RPi.GPIO as GPIO

lcd = LCD() #create LCD dispaly instance
lcd.backlight (False) #Turn off LCD backlight
lcd.clear()

for _ in range (6):
    for _ in range (2):
        
        lcd.backlight (True)
        time.sleep (0.2)
        lcd.backlight (False)
        time.sleep (0.2)
        
    time.sleep (1)

print("done")
