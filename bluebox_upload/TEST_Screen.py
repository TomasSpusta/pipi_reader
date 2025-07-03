from lcd_display_class import LCDController
from screen_manager import Screens
import asyncio
from gpiozero import Button


lcd = LCDController()
button = Button(21)
screens = Screens(lcd_controller=lcd)
instrument_name = "POKUS INSTRUMENT"
remaining_time = 5
selected_row = 0


async def button_press_handler():
    global selected_row
    while True:
        if button.is_pressed:
            selected_row = (selected_row + 1) % 4  # Cycle through rows
            await screens.button_menu(selected_row)
            await asyncio.sleep(0.3)  # Debounce delay
        await asyncio.sleep(0.1)


async def screen_test():
    await screens.welcome_screen(instrument_name=instrument_name)
    await screens.reservation_end_warning(remaining_time)
    await screens.welcome_screen(instrument_name=instrument_name)


async def main():
    await screens.button_menu(selected_row)
    await button_press_handler()
    # await screens.button_menu_extend_nok()
    # await screens.run_all_screens()
    # await screens.user_ok("John")
    pass


if __name__ == "__main__":
    asyncio.run(main())
