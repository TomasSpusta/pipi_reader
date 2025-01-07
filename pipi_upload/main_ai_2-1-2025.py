import asyncio
import logging
import random
from pathlib import Path

import networking
from gpiozero import Button
from lcd_display_class import LCDController
from model_classes import Instrument, Token, User
from rfid_reader_class import RFIDReader
from token_handler import verify_token

from datetime import datetime, timedelta
import time

from button_counter import ButtonCounter

# Initialize logging
logging.basicConfig(level=logging.INFO)


async def handle_user_session(
    rfid_reader: RFIDReader,
    lcd_controller: LCDController,
    instrument: Instrument,
    button,
):
    API_KEY = "ude9c6nezyr71i9vf3jdtye18vwdk81s"
    TOKEN_FILE = Path("token_data.json")

    phrases = [
        "Push the boundaries!",
        "Unleash your genius!",
        "Answers lie ahead!",
        "Discovery awaits!",
        "Keep exploring!",
        "Truth is out there!",
        "Find the unknown!",
    ]

    async def random_phase() -> str:
        phrase = random.choice(phrases)
        return phrase

    try:
        # card_id = await asyncio.wait_for(rfid_reader.read_card(), timeout=5)
        # Step 1: Read user card
        card_id = await rfid_reader.read_card()
        if not card_id:
            await lcd_controller.message(
                "Card reader issue.", "Please contact", "User office", display_time=5
            )
            logging.warning("No card detected.")
            return

        # Step 2: Compare card id and user database
        user = await networking.fetch_user_data(card_id)
        if not user:
            await lcd_controller.message(
                "Card not in database",
                "Please register it",
                "in booking system",
                display_time=3,
            )
            logging.warning(f"User not found for card ID: {card_id}")
            return

        phrase = await random_phase()
        await lcd_controller.message(user.name, "", phrase, display_time=5)

        logging.info(f"User {user.name} found. Starting session...")

        # Step 3: Vewrify token and verify, that user and reservation connection exists
        token = await verify_token(TOKEN_FILE, API_KEY)
        session = await networking.start_recording(
            user, instrument, token, session=None
        )

        if not session:
            logging.error("Failed to start recording session.")
            return

        session_container = {"session": session, "terminate": False}

        await lcd_controller.message("Recording is running")

        async def prolong_reservation(
            card_id: str,
            user: User,
            lcd_controller: LCDController,
            token: Token,
            session_container: dict,
        ):
            """
            Continuously listen for card swipes in session and prolong the reservation
            if the correct card is swiped.
            """
            while session_container["session"].remaining_time > 0:
                try:
                    # new_card_id = await rfid_reader.read_card_in_session()
                    # timeout = session_container['session'].remaining_time
                    new_card_id = await asyncio.wait_for(
                        rfid_reader.read_card_in_session(), timeout=15
                    )
                    print("Reader reset")

                    if new_card_id == card_id:
                        if session_container["session"].remaining_time > 15:
                            await lcd_controller.message(
                                "Session can be prolonged only 15 minutes before end",
                                display_time=3,
                            )
                        else:
                            session_container[
                                "session"
                            ] = await networking.start_recording(
                                user, instrument, token, session=None
                            )
                            print("Session prolonged")
                            await lcd_controller.message(
                                "Session prolonged by 15 minutes"
                            )
                    elif new_card_id is None:
                        print("No card")
                    else:
                        await lcd_controller.message("Unauthorized card")
                    await asyncio.sleep(0.5)

                except asyncio.TimeoutError:
                    print("Timeout Error in prolong reservation")
                    await asyncio.sleep(1)

                except Exception as e:
                    print(f"Error in prolong_reservation: {e}")
                    # Optionally handle errors, e.g., reset the reader or notify the user
                    await asyncio.sleep(1)

            print("Prolongation loop ended")

        async def monitor_and_update():
            """Handle button monitoring and session updates."""

            async with asyncio.TaskGroup() as tg:
                tg.create_task(
                    monitor_button(
                        rfid_reader,
                        button,
                        lcd_controller,
                        session_container,
                        instrument,
                        token,
                    )
                )
                tg.create_task(
                    update_session_time(lcd_controller, session_container, token)
                )
                # tg.create_task(prolong_reservation(card_id, user, lcd_controller, token, session_container))

        """
        if session_container['session'].remaining_time == 0:
            await lcd_controller.message(line1="Recording ended", display_time=5)
            return
        """

        print(
            f"session.remaining_time is {session_container['session'].remaining_time}"
        )
        await monitor_and_update()
        # await prolong_reservation (card_id, user, lcd_controller, token, session)
        logging.info("Session ended.")
        await lcd_controller.message(
            "Your session ended.", "See you next time.", display_time=3
        )

    except asyncio.TimeoutError:
        logging.warning("Timeout while waiting for card read.")
    except Exception as e:
        logging.error(f"Error during user session: {e}", exc_info=True)


async def update_session_time(
    lcd_controller: LCDController,
    # session:Session,
    session_container: dict,
    token: Token,
):
    refresh_rate = 5  # refresh rate of session info in seconds
    while (
        session_container["session"].remaining_time > 0
        and session_container["session"].ended_by_user is False
    ):
        await networking.fetch_reservation_info(token, session_container["session"])
        print(f"Update_session_time: {session_container['session'].remaining_time}")

        if (
            session_container["session"].remaining_time <= 5
            and session_container["session"].warning_sent is False
        ):
            print("Warning sent")
            await lcd_controller.message(
                "Your session will",
                f"end in {session_container['session'].remaining_time} minutes.",
                display_time=8,
            )
            session_container["session"].warning_sent = True

        await lcd_controller.message(
            "Recording is running",
            f"Remaining time: {session_container['session'].remaining_time}",
            "Prolong -> CARD",
            "End -> BUTTON",
            backlight=False,
        )

        await asyncio.sleep(refresh_rate)

    print("Session loop ended")
    session_container["terminate"] = True


async def monitor_button(
    rfid_reader: RFIDReader,
    button: Button,
    lcd_controller: LCDController,
    session_container: dict,
    instrument: Instrument,
    token: Token,
):
    """Monitor button for a 5-second hold and showing that user ends the session"""
    count = 0
    hold_time = 0
    delay = 5
    click_times = []
    double_click_window = 0.5
    button_counter = ButtonCounter()

    while session_container["session"].remaining_time > 0:
        if button.is_pressed:
            """
            Monitor button press count:
                when pressed =  Show button menu
                    in menu double-click = Show scan card menu -> prolong session
                    in menu hold 5 seconds = End session
                    in menu when nothing for 3 seconds, continue session 
            """

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
                card_read = await rfid_reader.card_reader_time_slot(10)
                print(card_read)

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
        """
        await asyncio.sleep(0.2)

    print("Button deactivated")
    session_container["terminate"] = True


async def main_loop():
    try:
        button = Button(21)
        lcd_controller = LCDController()
        rfid_reader = RFIDReader()
        # session = Session()
        await networking.fetch_ip()
        mac = await networking.fetch_mac()
        # instrument_mac_address = "e4:5f:01:ea:99:17"
        API_KEY = "ude9c6nezyr71i9vf3jdtye18vwdk81s"  #
        TOKEN_FILE = Path("token_data.json")

        await verify_token(TOKEN_FILE, API_KEY)
        # token = await initiate_token(API_KEY, TOKEN_FILE)
        instrument = await networking.fetch_instrument_data(mac)

        while True:
            await lcd_controller.welcome_screen(instrument=instrument)
            await handle_user_session(rfid_reader, lcd_controller, instrument, button)
            await asyncio.sleep(1)  # Sleep briefly to prevent tight looping
        # for task in asyncio.all_tasks():
        #    print(f"Task: {task}, State: {task.get_stack()}")

    finally:
        print("Finally block")
        await rfid_reader.cleanup()
        await lcd_controller.cleanup()


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
