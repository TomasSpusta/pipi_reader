import asyncio
import logging
from pathlib import Path
from gpiozero import Button
from lcd_display_class import LCDController
from model_classes import Instrument, Token, User, SessionStatus, Session
from rfid_reader_class import RFIDReader
from token_handler import verify_token
import networking
import keys

# Initialize logging
logging.basicConfig(level=logging.INFO)


async def fetch_instrument():
    """Fetch the instrument details using the MAC address."""
    mac = await networking.fetch_mac()
    return await networking.fetch_instrument_data(mac)


async def welcome_and_wait_for_card(lcd_controller, rfid_reader, instrument):
    """Display the welcome screen and wait for a card swipe."""
    await lcd_controller.welcome_screen(instrument)
    return await rfid_reader.read_card()


async def verify_user(card_id, lcd_controller):
    """Verify if the card ID corresponds to a valid user."""
    user = await networking.fetch_user_data(card_id)
    if not user:
        await lcd_controller.message(
            "Card not registered.", "Please register in system.", display_time=3
        )
    return user


async def start_session(user, instrument, token, lcd_controller):
    """Start a recording session for the user."""
    session = await networking.start_recording(user, instrument, token)
    if not session:
        await lcd_controller.message(
            "Session start failed.", "Try again later.", display_time=1
        )
    else:
        await lcd_controller.message(
            "Session started.", "Enjoy your work!", display_time=1
        )
    return session


async def display_session_info(
    lcd_controller, session_container: Session, session_flags, token
):
    """Display session information continuously."""
    while session_container.remaining_time > 0:
        if session_flags["display_session_info"]:
            await networking.fetch_reservation_info(token, session_container)
            print(f"Remaining session time: {session_container.remaining_time}")
            await lcd_controller.message(
                "Recording in progress",
                f"Time left: {session_container.remaining_time} mins",
                "Prolong -> CARD",
                "End -> BUTTON",
            )
            await asyncio.sleep(5)
        await asyncio.sleep(0.5)


async def handle_button_menu(
    button: Button,
    rfid_reader: RFIDReader,
    session: Session,
    lcd_controller: LCDController,
    token: Token,
    instrument: Instrument,
    user: User,
    session_flags,
):
    """Handle interactions in the button menu."""

    """
    +1 press    -> enter menu
                -> wait to card swipe with timeout
    +1 press    -> end reservation question, timeout 10 s with timer
    +1 press    -> end reservation api
    
    """

    press_count = 0
    timeout = 15
    scan_card_timeout = 10
    start_time = asyncio.get_event_loop().time()
    current_time = asyncio.get_event_loop().time()
    session_flags["display_session_info"] = False
    timer_started = False
    timer_start_time = None
    press_detection_time = 10

    """
        if current_time - start_time > timeout:
            await lcd_controller.message(
                "Timeout.", "Returning to session.", display_time=3
            )
            break  # Exit the button menu after timeout
"""
    while session.remaining_time > 0:
        if button.is_pressed:
            session_flags["display_session_info"] = False
            if not timer_started:
                timer_started = True
                timer_start_time = asyncio.get_event_loop().time()

            print(f"Press count: {press_count}")
            await lcd_controller.message(
                "1 press -> prolong",
                "3 presses -> end",
                "4+ presses -> back",
                f"Your presses: {press_count}",
                display_time=0.1,
            )
            press_count += 1
            await asyncio.sleep(0.2)

        elif timer_started:
            elapsed_time = asyncio.get_event_loop().time() - timer_start_time
            if elapsed_time >= press_detection_time:
                match press_count:
                    case 1:
                        pass
                    case 2:
                        # Single press: Scan card to prolong
                        await lcd_controller.message(
                            "Scan your card to prolong.", display_time=0.5
                        )
                        card_id = await rfid_reader.card_reader_time_slot(
                            scan_card_timeout
                        )
                        if card_id == user.card_id:
                            await networking.start_recording(
                                user=user,
                                instrument=instrument,
                                token=token,
                            )
                            await lcd_controller.message(
                                "Session prolonged.", display_time=2
                            )
                        elif card_id is None:
                            await lcd_controller.message(
                                "No card detected.", display_time=2
                            )
                        else:
                            await lcd_controller.message("Wrong card", display_time=2)

                    case 3:
                        # Double press: Confirm stop reservation
                        pass

                    case 4:
                        # Triple press: Stop reservation
                        session.ended_by_user = True
                        await lcd_controller.message(
                            "Stopping reservation.",
                            "Session ended.",
                            display_time=3,
                        )
                        await networking.stop_recording(session, instrument, token)
                        # return  # Exit button menu

                    case _:
                        # Reset for unexpected press counts
                        await lcd_controller.message(
                            "Returning to session.", display_time=2
                        )

                # Reset press count and timer
                press_count = 0
                timer_started = False
                print("Returning to the session")
                session_flags["display_session_info"] = True

        await asyncio.sleep(0.1)


"""
            print(f"Press count: {press_count}")
            press_count += 1
            
            match press_count:
                case 0:
                    session_flags["display_session_info"] = True
                case 1:
                    await lcd_controller.message(
                        "Button Menu",
                        "CARD -> Prolong",
                        "PRESS -> End",
                        display_time=0.5,
                    )

                    card_id = await rfid_reader.card_reader_time_slot(scan_card_timeout)
                    if card_id == user.card_id:
                        await networking.start_recording(
                            user=user,
                            instrument=instrument,
                            token=token,
                        )
                        await lcd_controller.message(
                            "Session prolonged.", display_time=2
                        )
                        session_flags["display_session_info"] = True
                        press_count = 0
                    elif card_id is None:
                        pass
                        press_count = 0
                        session_flags["display_session_info"] = True
                    else:
                        press_count = 0
                        await lcd_controller.message("Wrong card", display_time=2)
                        session_flags["display_session_info"] = True
                case 2:
                    # end question with timeout
                    pass
                case 3:
                    # stop reservation api -> end program
                    pass
                case _:
                    session_flags["display_session_info"] = True
        await asyncio.sleep(0.1)

"""


"""
            current_time = asyncio.get_event_loop().time()
            await lcd_controller.message(
                "Button Menu", "CARD -> Prolong", "HOLD 5s -> End", display_time=0.5
            )
            session_flags["display_session_info"] = True

            if button_hold_start is None:
                button_hold_start = current_time  # Start tracking hold time
            elif current_time - button_hold_start >= 5:  # Held for 5 seconds
                session.ended_by_user = True
                await lcd_controller.message(
                    "Stopping reservation.", "Session ended.", display_time=3
                )
                await networking.stop_recording(session, instrument, token)
                session_flags["display_session_info"] = False

            else:
                button_hold_start = None  # Reset hold time if the button is released

            if (
                button_hold_start and current_time - button_hold_start < 1
            ):  # Single press
                await lcd_controller.message(
                    "Scan your card to prolong.", display_time=3
                )
                
                    await lcd_controller.message("Session prolonged.", display_time=3)
                    button_hold_start = None  # Reset after prolongation
                    session_flags["display_session_info"] = True
                else:
                    session_flags["display_session_info"] = True

        await asyncio.sleep(0.1)  # Small delay for smooth button monitoring
"""

"""
            
            
            start_time = asyncio.get_event_loop().time()  # Record the start time
            session_flags["display_session_info"] = False

            current_time = asyncio.get_event_loop().time()  # Get the current time
            if current_time - start_time > timeout:
                await lcd_controller.message(
                    "Timeout.", "Returning to session.", display_time=3
                )
                session_flags["display_session_info"] = True

            print(f"Session_flag: {session_flags}")
            press_time += 1
            if press_time >= 5:  # Held for 5 seconds
                session.ended_by_user = True
                await lcd_controller.message(
                    "Session ended.", "Thank you!", display_time=3
                )
                await networking.stop_recording(session, instrument, token)
                break  # Exit button menu and terminate session
        else:
            press_time = 0

        if press_time == 1:  # Single press
            await lcd_controller.message("Scan your card to prolong.", display_time=0.5)
            card_id = await rfid_reader.card_reader_time_slot(10)

            if card_id == user.card_id:
                await networking.start_recording(
                    user=user,
                    instrument=instrument,
                    token=token,
                )
                await lcd_controller.message("Session prolonged.", display_time=3)
            press_time = 0  # Reset press time and continue monitoring
            session_flags["display_session_info"] = True
            print(f"Session_flag: {session_flags}")

        await asyncio.sleep(0.05)
"""


async def main_loop():
    """Main application loop."""
    button = Button(21, hold_time=2)
    lcd_controller = LCDController()
    rfid_reader = RFIDReader()
    token_file = keys.TOKEN_FILE
    api_key = keys.API_KEY

    await verify_token(token_file, api_key)
    instrument = await fetch_instrument()

    while True:
        card_id = await welcome_and_wait_for_card(
            lcd_controller, rfid_reader, instrument
        )
        if not card_id:
            continue

        user = await verify_user(card_id, lcd_controller)
        if not user:
            continue

        token = await verify_token(token_file, api_key)
        session = await start_session(user, instrument, token, lcd_controller)
        if not session:
            continue

        session_container = {
            "session": session,
        }
        session_flags = {
            "display_session_info": True
        }  # Flag to manage session info display state

        await asyncio.gather(
            display_session_info(
                lcd_controller, session_container["session"], session_flags, token
            ),
            handle_button_menu(
                button=button,
                rfid_reader=rfid_reader,
                session=session_container["session"],
                lcd_controller=lcd_controller,
                token=token,
                instrument=instrument,
                user=user,
                session_flags=session_flags,
            ),
        )

        if (
            session_container["session"].ended_by_user
            or session_container["session"].remaining_time <= 0
        ):
            session_flags["display_session_info"] = False
            await lcd_controller.message(
                "Session ended.", "See you next time!", display_time=3
            )


if __name__ == "__main__":
    asyncio.run(main_loop())
