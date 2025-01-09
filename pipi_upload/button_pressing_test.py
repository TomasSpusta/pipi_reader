import asyncio
import logging
import random
import time
from datetime import datetime, timedelta
from pathlib import Path
from lcd_display_class import LCDController


from button_counter import ButtonCounter
from gpiozero import Button


async def monitor_button_test(button: Button, lcd_controller: LCDController):
    """Monitor button for a 5-second hold and showing that user ends the session"""
    count = 0
    hold_time = 0
    delay = 5
    click_times = []
    double_click_window = 0.5
    button_counter = ButtonCounter()

    while True:
        # Wait for the button to be pressed
        await asyncio.sleep(0.01)  # Small delay to avoid busy waiting

        if button.is_pressed:
            print("Button pressed")
            count += 1

            await asyncio.sleep(0.2)  # Debounce to avoid rapid multiple counts

            if count == 1:
                print(f"Counter: {count}")
                asyncio.create_task(lcd_controller.add_message(2, ["Button menu"], 3))

            elif count == 2:
                print(f"Counter: {count}")
                count = 0
                await lcd_controller.add_message(1, ["Please scan card"], 3)


async def counter():
    counter = 0
    while True:
        counter += 1
        return counter


async def main_loop():
    try:
        instrument = "instrument 1"
        button = Button(21)
        lcd_controller = LCDController(default_message=[instrument])
        # asyncio.create_task(lcd_controller.display_loop())

        while True:
            button_task = monitor_button_test(button, lcd_controller)
            lcd_task = lcd_controller.display_loop()
            await asyncio.gather(button_task, lcd_task)
            await asyncio.sleep(0.2)  # Sleep briefly to prevent tight looping
        # for task in asyncio.all_tasks():
        #    print(f"Task: {task}, State: {task.get_stack()}")

    finally:
        print("Finally block")


# Entry point
if __name__ == "__main__":
    try:
        asyncio.run(main_loop())

    except KeyboardInterrupt:
        print("Ended by CTRL + C")

    except asyncio.CancelledError:
        print("Program cancelled")

    except Exception as e:
        print(f"Unexpected error: {e}")


'''
        time_now = datetime.now()
        if button.is_pressed:
            press_counter = await button_counter.button_pressed()
            print(press_counter)
            await asyncio.sleep(0.2)

            if press_counter == 1:
                await lcd_controller.message(
                    "If you wish to prolong reservation press button.",
                    display_time=3,
                    blocking=False,
                )

            if press_counter == 2:
                await lcd_controller.message(
                    "Please scan your card",
                    display_time=5,
                    blocking=True,
                )
            """


"""
            time_delta = timedelta(seconds=2)
            button_time = float(button.active_time)
            print(button_time)
            # await asyncio.sleep(0.2)
            count += 1

            if count == 3:
                time_later = datetime.now()
                print((time_later - time_now))
                if (time_later - time_now) < time_delta:
                    print((time_later - time_now))
                    print("Doubleclick")
                    await lcd_controller.message(
                        "Do you want to prolong reservation?",
                        display_time=3,
                        blocking=True,
                    )
                    count = 0
                else:
                    count = 0
            elif count > 3:
                print("Button reset")
                count = 0
            print(count)

            if button_time > 5:
                await lcd_controller.message(
                    "Session ended by user", display_time=3, blocking=True
                )
                print("Ended by user")
"""
"""
            if button_time < 1:
                await lcd_controller.message(
                    "Button pressed.",
                    "Prolong->hold + swipe card",
                    "END->hold more",
                    display_time=3,
                )

            if 1 <= button_time <= 10:
                await lcd_controller.message(
                    "Do you want to prolong reservation?",
                    display_time=1,
                )
                card_read = await rfid_reader.card_reader_time_slot(10)
                print(card_read)

            if button_time > 10:
                await lcd_controller.message("Session ended by user", display_time=1)
                # print ("")
            """

"""
        
        
        
        if button.is_pressed:  # Replace with actual button press detection
            current_time = asyncio.get_event_loop().time()
            
            # Handle double-click detection
            click_times.append(current_time)
            click_times = [
                t for t in click_times if current_time - t <= double_click_window
            ]

            if len(click_times) == 2:  # Detected double-click
                click_times.clear()
                await lcd_controller.message(
                    "Double-click detected.",
                    "Listening for card...",
                    display_time=2,
                )

                # Open time slot for card reading
                card_read = await rfid_reader.card_reader_time_slot(10)
                if card_read:
                    await lcd_controller.message(
                        "Card processed!",
                        f"Card ID: {card_read}",
                        display_time=3,
                    )
                else:
                    await lcd_controller.message(
                        "No card detected.", "Continuing session.", display_time=3
                    )
                continue
                        
            if hold_time == 0:
                await lcd_controller.message (
                    "Button pressed.",
                    "If you want", 
                    "to end session,",
                    f"hold it for {delay} sec.",
                    display_time=1
                    )
                
            hold_time += 1
            if button.is_held >= delay:
                logging.info(f"Button held for {delay} seconds. Ending session")
                session_container['session'].ended_by_user = True
                await lcd_controller.message ("Session ended","by user", display_time=5)
                await networking.stop_recording(session_container['session'], instrument, token)
                print (f"Button Stop recording session time: {session_container['session'].remaining_time}")
                
                hold_time = 0
                return
        
        else:
            hold_time = 0
'''
