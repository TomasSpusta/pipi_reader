import asyncio
import logging
from pathlib import Path

import keys
import networking
from gpiozero import Button
from lcd_display_class import LCDController
from model_classes import Instrument, Session, Token, User
from rfid_reader_class import RFIDReader
from screen_manager import Screens
from token_handler import verify_token, check_expiration

# Initialize logging
logging.basicConfig(level=logging.INFO)


async def fetch_instrument():
    """Fetch the instrument details using the MAC address."""
    mac = await networking.fetch_mac()
    return await networking.fetch_instrument_data(mac)


async def welcome_and_wait_for_card(
    screens: Screens, rfid_reader: RFIDReader, instrument: Instrument
):
    """Display the welcome screen and wait for a card swipe."""
    await screens.welcome_screen(instrument.name)
    return await rfid_reader.read_card()


async def verify_user(card_id: str, screens: Screens):
    """Verify if the card ID corresponds to a valid user."""
    await screens.checking_user()
    user = await networking.fetch_user_data(card_id)
    if not user:
        await screens.user_not_in_database()
    await screens.user_ok(user_name=user.name)
    return user


async def start_session(
    user: User, instrument: Instrument, token: Token, screen: Screens
):
    """Start a recording session for the user."""
    session = await networking.start_recording(user, instrument, token)
    if not session:
        await screen.reservation_nok()
    else:
        await screen.reservation_ok()
    return session


async def display_session_info(
    screen: Screens, session_container: Session, session_flags, token: Token
):
    """Display session information continuously."""
    while session_container.remaining_time > 0:
        if (
            session_flags["display_session_info"]
            and session_container.remaining_time > 0
        ):
            await networking.fetch_reservation_info(token, session_container)
            print(f"Remaining session time: {session_container.remaining_time}")
            await screen.in_session(
                remaining_session_time=session_container.remaining_time
            )
            # await asyncio.sleep(5)
            if await check_expiration(token) is False:
                token = await verify_token()
        await asyncio.sleep(0.5)


async def handle_button_menu(
    button: Button,
    rfid_reader: RFIDReader,
    session: Session,
    screen: Screens,
    token: Token,
    instrument: Instrument,
    user: User,
    session_flags,
):
    """Handle interactions in the button menu."""

    selected_row = 0
    scan_card_timeout = 5
    timer_started = False
    timer_start_time = None
    press_detection_time = 3

    while session.remaining_time > 0:
        if button.is_pressed:
            timer_started = False
            session_flags["display_session_info"] = False
            if not timer_started:
                timer_started = True
                timer_start_time = asyncio.get_event_loop().time()

            await screen.button_menu(selected_row)
            print(f"Selected row: {selected_row + 1}")

            selected_row = (selected_row % 4) + 1

            await asyncio.sleep(0.2)

        elif timer_started:
            elapsed_time = asyncio.get_event_loop().time() - timer_start_time
            # print(f"Elapsed time: {elapsed_time}")
            if elapsed_time >= press_detection_time:
                match selected_row:
                    case 1:
                        print("Back selected")
                        # Back to session
                        pass

                    case 2:
                        print("Extend selected")
                        if session.remaining_time < 15:
                            # Single press: Scan card to prolong
                            await screen.button_menu_extend()
                            card_id = await rfid_reader.card_reader_time_slot(
                                scan_card_timeout
                            )
                            if card_id == user.card_id:
                                await networking.start_recording(
                                    user=user,
                                    instrument=instrument,
                                    token=token,
                                )
                                await screen.button_menu_extend_ok()
                            elif card_id is None:
                                pass
                            else:
                                await screen.button_menu_extend_bad_card()
                        else:
                            await screen.button_menu_extend_not_yet()

                    case 3:
                        print("Supervisor selected")
                        # Supervisor mode
                        # for future step in of supervisor.
                        pass

                    case 4:
                        print("End selected")
                        await networking.stop_recording(session, instrument, token)
                        await screen.session_ended_by_user()
                        session.ended_by_user = True

                    case _:
                        # Reset for unexpected press counts
                        pass

                # Reset press count and timer
                selected_row = 0
                timer_started = False
                print("Returning to the session")
                session_flags["display_session_info"] = True

        await asyncio.sleep(0.1)


async def main_loop():
    """Main application loop."""
    button = Button(21)
    lcd_controller = LCDController()
    screens = Screens(lcd_controller=lcd_controller)
    rfid_reader = RFIDReader()

    await networking.safe_api_call(verify_token, screen=screens)
    instrument = await networking.safe_api_call(fetch_instrument, screen=screens)

    while True:
        card_id = await networking.safe_api_call(
            welcome_and_wait_for_card,
            screen=screens,
            screens=screens,
            rfid_reader=rfid_reader,
            instrument=instrument,
        )
        if not card_id:
            continue

        user = await verify_user(card_id, screens)
        if not user:
            continue

        token = await verify_token()
        session = await start_session(user, instrument, token, screens)
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
                screens, session_container["session"], session_flags, token
            ),
            handle_button_menu(
                button=button,
                rfid_reader=rfid_reader,
                session=session_container["session"],
                screen=screens,
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
