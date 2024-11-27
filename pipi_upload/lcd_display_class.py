
from RPLCD.i2c import CharLCD
import time


class LCDDisplay:
    def __init__(self, i2c_address=0x27):
        self.lcd = CharLCD(
            i2c_expander='PCF8574', address=i2c_address, port=1, cols=20, rows=4, dotsize=8)

    def write(self, text, row):
        self.lcd.cursor_pos = (row-1, 0)
        self.lcd.write_string = (text)

    def message(self, line1, line2, line3, line4, backlight):
        self.lcd.backlight_enabled = backlight
        if self.clear == True:
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
