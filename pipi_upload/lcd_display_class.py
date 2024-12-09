
from RPLCD.i2c import CharLCD
import time
from model_classes import Instrument
import asyncio
from typing import Optional

#initialize the LCD display, (expander chip, port)
class LCDController:
    def __init__(self, address = 0x27, chip = 'PCF8574'):
        self.lcd = CharLCD(chip,address)

    async def write(self,text, row):
        if text:
            #await asyncio.to_thread(self.lcd.cursor_pos.__setattr__,(row-1, 0))
            await asyncio.to_thread(setattr, self.lcd, "cursor_pos",(row-1, 0))
            await asyncio.to_thread(self.lcd.write_string, text)

    async def message(
        self, 
        line1: Optional[str], line2:str = None, line3:str =None, line4:str = None, backlight:bool =True, clear:bool=True):
        await asyncio.to_thread(setattr, self.lcd, "backlight_enabled", backlight)
        if clear is True:
            await asyncio.to_thread(self.lcd.clear)
        await self.write(line1, 1)
        await self.write(line2 or "", 2)
        await self.write(line3 or "", 3)
        await self.write(line4 or "", 4)

    async def backlight(self, status:bool):
        await asyncio.to_thread(setattr, self.lcd, "backlight_enabled", status)

    async def clear(self):
        await asyncio.to_thread(self.lcd.clear)

    async def flashing(self, interval, number_of_flashes):
        for _ in range(number_of_flashes):
            await asyncio.sleep(interval)
            await asyncio.to_thread(setattr, self.lcd, "backlight_enabled", True)
            await asyncio.sleep(interval)
            await asyncio.to_thread(setattr, self.lcd, "backlight_enabled", False)

    async def welcome_screen(self, instrument:Instrument):
        message_template = [
            "Welcome at",
            f"{instrument.name}",
            "Please log in",
            "with your card."
        ]        
        await self.message(*message_template)
    
    async def cleanup(self):
        await asyncio.to_thread(setattr, self.lcd, "backlight_enabled", False)
        await asyncio.to_thread(self.lcd.clear)
        
    
    
            
    