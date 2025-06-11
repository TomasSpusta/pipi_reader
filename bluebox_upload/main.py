import asyncio
import logging
from pathlib import Path

from logger import Logger
from datetime import datetime
#import bluebox_upload.config as config
import networking
from gpiozero import Button
from lcd_display import LCDController
from model_classes import Instrument, Session, Token, User
from rfid_reader import RFIDReader
from screen_manager import Screens
from token_handler import verify_token, check_expiration
from button_handler import buttons_handling


async def fetch_instrument():
    """Fetch the instrument details using the MAC address."""
    ip = await networking.fetch_ip()
    mac = await networking.fetch_mac()
    return await networking.fetch_instrument_data(mac, ip)


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
    warning_sent = False
    while session_container.remaining_time > 0 and not session_container.ended_by_user:
        if (
            session_flags["display_session_info"]
            and session_container.remaining_time > 0
        ):
            await networking.fetch_recording_info(token, session_container)
            # print(f"Remaining session time: {session_container.remaining_time}")
            await screen.in_session(
                remaining_session_time=session_container.remaining_time
            )
            # await asyncio.sleep(5)

            token = await networking.safe_api_call(
                verify_token, error_screen=screen, logger=None
            )
            if session_container.remaining_time < 5 and warning_sent is False:
                print("Warning sent")
                await screen.session_end_warning(session_container.remaining_time)
                warning_sent = True
        await asyncio.sleep(0.5)




async def handle_button_menu(
    stop_reservation_btn: Button,
    #extend_reservation_btn = Button,
    rfid_reader: RFIDReader,
    session: Session,
    screen: Screens,
    token: Token,
    instrument: Instrument,
    user: User,
    session_flags,
):
    """Handle interactions in the stop_reservation_btn menu."""
    #extend_reservation_btn = Button()

    selected_row = 0
    scan_card_timeout = 5
    timer_started = False
    timer_start_time = None
    press_detection_time = 3

    while session.remaining_time > 0 and not session.ended_by_user:
        if stop_reservation_btn.is_pressed:
            #extend_reservation_btn = Button()
            timer_started = False
            session_flags["display_session_info"] = False
            if not timer_started:
                timer_started = True
                timer_start_time = asyncio.get_event_loop().time()

            await screen.button_menu(selected_row)
            # print(f"Selected row: {selected_row + 1}")

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
                                # Maybe log the session extension?
                            elif card_id is None:
                                pass
                            else:
                                await screen.button_menu_extend_bad_card()
                        else:
                            await screen.extend_not_yet()

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
                # print("Returning to the session")
                session_flags["display_session_info"] = True

        await asyncio.sleep(0.1)


# TODO: DONE -> Error messages for all functions
# TODO: DONE -> Loging feature to google disc
# TODO: What to log:
"""
What columns/data I want to log in:
    errors - every one.
    initialization of bluebox - when started
    session start
    session end
    user
    card swipes
    session extended
    
"""

# TODO: DONE -> Include card correction, when it has only 9 characters


async def main_loop():
    """Main application loop."""
    stop_btn = Button(21)
    extend_btn = Button(13)
    lcd_controller = LCDController()
    screens = Screens(lcd_controller=lcd_controller)
    rfid_reader = RFIDReader()

    await screens.starting_screen()

    token: Token = await networking.safe_api_call(
        verify_token, error_screen=screens, logger=None
    )

    instrument: Instrument = await networking.safe_api_call(
        fetch_instrument, error_screen=screens, logger=None
    )
    # print(f"{instrument.mac_address} {instrument.name}")
    logger = Logger(instrument.mac_address, instrument.name)
    await logger.initialize()
    await logger.insert_new_row()

    await logger.write_log(1, datetime.now())
    await logger.write_log(2, instrument.ip)
    await logger.write_log(5, instrument.name)
    await logger.write_log(9, token.expiration)

    while True:
        card_id = await networking.safe_api_call(
            welcome_and_wait_for_card,
            error_screen=screens,
            logger=logger,
            screens=screens,
            rfid_reader=rfid_reader,
            instrument=instrument,
        )
        await logger.insert_new_row()
        if not card_id:
            continue

        user: User = await networking.safe_api_call(
            verify_user,
            error_screen=screens,
            logger=logger,
            card_id=card_id,
            screens=screens,
        )

        if not user:
            await logger.write_log(7, card_id, datetime.now())
            continue
        else:
            # print(f"user: {user}")
            await logger.write_log(8, user.full_name, datetime.now())

        # token = await verify_token()
        session: Session = await networking.safe_api_call(
            start_session,
            error_screen=screens,
            logger=logger,
            user=user,
            instrument=instrument,
            token=token,
            screen=screens,
        )
        await logger.write_log(10, datetime.now())
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
            buttons_handling(
                stop_btn=stop_btn,
                extend_btn=extend_btn,
                #rfid_reader=rfid_reader,
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
            if session_container["session"].ended_by_user:
                await logger.write_log(11, datetime.now(), "Ended by user")
            else:
                await screens.session_ended_by_timeout()
                await logger.write_log(11, datetime.now(), "Ended by time")


if __name__ == "__main__":
    asyncio.run(main_loop())
