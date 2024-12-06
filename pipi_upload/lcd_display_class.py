
from RPLCD.i2c import CharLCD
import time
from model_classes import Instrument
import asyncio

class LCDDisplay:
    def __init__(self):
        self.lcd = CharLCD(            i2c_expander='PCF8574', address=0x27)

    async def write(self, text, row):
        self.lcd.cursor_pos = (row-1, 0)
        self.lcd.write_string = (text)

    async def message(self, line1:str, line2:None, line3:None, line4:None, backlight:bool, clear:bool):
        self.lcd.backlight_enabled = backlight
        if clear is True:
            self.lcd.clear()
        self.write(str(line1), 1)
        self.write(str(line2), 2)
        self.write(str(line3), 3)
        self.write(str(line4), 4)

    def backlight(self, status):
        self.lcd.backlight_enagled = status

    def clear(self):
        self.lcd.clear()

    def flashing(self, interval, number_of_flashes):
        for _ in range(number_of_flashes):
            time.sleep(interval)
            self.lcd.backlight_enabled = True
            time.sleep(interval)
            self.lcd.backlight_enabled = False
    
    async def welcome_screen(self, instrument:Instrument):
        await self.message (
        line1= "Welcome at",
        line2= instrument.name,
        line3= "plaease log in" ,
        line4= "with your card.",
        backlight=True,
        clear=True
        )
            
            
        