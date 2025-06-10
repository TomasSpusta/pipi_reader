import asyncio
from RPLCD.i2c import CharLCD
from gpiozero import Button

# Setup LCD and Button
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4)
button = Button(21)  # GPIO pin 17 for the button


async def update_lcd():
    """Coroutine to update the LCD display."""
    counter = 0
    while True:
        lcd.clear()
        lcd.write_string(f"Counter: {counter}")
        counter += 1
        await asyncio.sleep(1)  # Update the display every second


async def monitor_button():
    """Coroutine to handle button presses."""
    while True:
        if button.is_pressed:
            lcd.clear()
            lcd.write_string("Button Pressed!")
            await asyncio.sleep(0.5)  # Debounce delay
        await asyncio.sleep(0.1)  # Check button status frequently


async def main():
    """Main entry point for the asyncio loop."""
    # Schedule both coroutines
    lcd_task = asyncio.create_task(update_lcd())
    button_task = asyncio.create_task(monitor_button())

    # Run tasks concurrently
    await asyncio.gather(lcd_task, button_task)

# Run the asyncio event loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    lcd.clear()
    lcd.write_string("Goodbye!")
