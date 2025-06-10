from RPLCD.i2c import CharLCD
import asyncio


class LCDController:
    def __init__(self, address=0x27, chip="PCF8574"):
        # Initialize the LCD with the given chip and address, setting dimensions for a 4x20 display
        self.lcd = CharLCD(chip, address, cols=20, rows=4)

    async def message(self, lines, clear=True, backlight=True):
        """
        Display a message on the LCD.

        Parameters:
        - lines (list of str): List of up to 4 strings, each representing one row.
        - clear (bool): Whether to clear the display before writing.
        - backlight (bool): Whether to enable the backlight.
        """
        try:
            if backlight:
                await asyncio.to_thread(setattr, self.lcd, "backlight_enabled", True)
            if clear:
                await asyncio.to_thread(self.lcd.clear)

            # Write each line to the appropriate row
            for row, line in enumerate(lines[:4]):  # Maximum 4 rows
                # Ensure the cursor position is set for the current row
                await asyncio.to_thread(setattr, self.lcd, "cursor_pos", (row, 0))
                # Write the line, truncated to 20 characters to fit the LCD width
                await asyncio.to_thread(self.lcd.write_string, line[:20])

        except Exception as e:
            print(f"Error displaying message on LCD: {e}")

    async def clear_display(self):
        """Clear the LCD display."""
        try:
            await asyncio.to_thread(self.lcd.clear)
        except Exception as e:
            print(f"Error clearing LCD display: {e}")

    async def set_backlight(self, enable):
        """Enable or disable the LCD backlight."""
        try:
            await asyncio.to_thread(setattr, self.lcd, "backlight_enabled", enable)
        except Exception as e:
            print(f"Error setting LCD backlight: {e}")

    async def cleanup(self):
        """Perform cleanup tasks for the LCD, such as turning off the backlight and clearing the display."""
        try:
            await self.clear_display()
            await self.set_backlight(False)
        except Exception as e:
            print(f"Error during LCD cleanup: {e}")
