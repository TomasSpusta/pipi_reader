import asyncio
from gpiozero import Button
from RPLCD.i2c import CharLCD
import aiohttp

# Initialize LCD (adjust I2C address and port for your setup)
lcd = CharLCD("PCF8574", 0x27, cols=20, rows=4)

# Initialize Button
button = Button(21, hold_time=2)  # GPIO pin 18, with 2-second hold detection


# Global variables
run_counter = 0
in_menu = False  # Tracks whether we're in the "Button Menu"


async def update_counter():
    """Continuously updates the run counter on the LCD."""
    global run_counter, in_menu
    while True:
        if not in_menu:  # Only update the counter if not in the menu
            run_counter += 1
            lcd.clear()
            lcd.write_string(f"Run Count:\n{run_counter}")
        await asyncio.sleep(1)  # Update every second


async def wait_for_button_press():
    """Asynchronous wrapper for button press detection."""
    while True:
        await asyncio.to_thread(button.wait_for_press)
        yield  # Yield control to indicate a button press


async def handle_button_presses():
    """Handles button presses to switch between counter, menu, and countdown."""
    global in_menu
    async for _ in wait_for_button_press():
        if not in_menu:
            # Enter the "Button Menu"
            in_menu = True
            await show_button_menu()
        else:
            # Trigger the countdown
            await start_countdown()
            in_menu = False  # Exit the menu after the countdown


async def show_button_menu():
    """Displays the 'Button Menu' and waits for a timeout or additional button press."""
    global in_menu
    lcd.clear()
    lcd.write_string("Button Menu")

    try:
        # Wait for another button press or timeout after 5 seconds
        await asyncio.wait_for(wait_for_button_press().__anext__(), timeout=5)
        # If a button is pressed, trigger the countdown
        await start_countdown()
    except asyncio.TimeoutError:
        # Timeout occurred, exit the menu and return to the counter
        in_menu = False
        lcd.clear()
        lcd.write_string("Exiting Menu")
        await asyncio.sleep(1)


async def start_countdown():
    """Starts a countdown from 10 on the LCD."""
    for i in range(10, 0, -1):
        # lcd.clear()
        # lcd.write_string(f"Countdown:\n{i}")
        print(i)
        await asyncio.sleep(1)
    # lcd.clear()
    # lcd.write_string("Done!")
    await asyncio.sleep(2)  # Keep "Done!" displayed for 2 seconds


async def main():
    """Main coroutine to run all tasks."""
    # Create tasks for all concurrent operations
    counter_task = asyncio.create_task(update_counter())
    button_task = asyncio.create_task(handle_button_presses())
    await asyncio.gather(counter_task, button_task)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    lcd.clear()
    print("Program exited cleanly.")
