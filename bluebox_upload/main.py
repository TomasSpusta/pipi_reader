import asyncio
from states.init_state import InitState

# from states.test_state import TestState
from app_context import AppContext
from screen_manager import Screens
from lcd_display import LCDController
from rfid_reader import RFIDReader
from api_client import APIClient
from gpiozero import Button
from networking import network_monitor


async def main():
    context = AppContext()
    context.state = InitState()
    context.screens = Screens(LCDController())
    context.rfid_reader = RFIDReader()
    context.api = APIClient()
    context.stop_btn = Button(21, hold_time=0.1, bounce_time=0.05)
    context.extend_btn = Button(13, hold_time=0.1, bounce_time=0.05)
    context.lock = asyncio.Lock()

    asyncio.create_task(network_monitor(context.screens, context))

    while True:
        context.state = await context.state.run(context)
        print(f"Lcd in use:{context.flags.lcd_in_use}, in main.")
        print(f"Current state: {context.state.__module__}")


if __name__ == "__main__":
    asyncio.run(main())


"""
TODO: verify token before api calls
TODO: continuous wifi check

"""


'''
import asyncio
import os
from logger import Logger
from datetime import datetime
import networking
from gpiozero import Button
from lcd_display import LCDController
from model_classes import Instrument, Session, Token, User
from rfid_reader import RFIDReader
from screen_manager import Screens
from token_handler import verify_token
from button_handler import buttons_handling
from NetworkGuard import NetworkGuard
from AppContext import AppContext, AppState, AppFlags
from state_utils import transition_to
from state_renderer import StateRenderer

"""
# TODO: 



"""


async def welcome_and_wait_for_card(
    *,
    screens: Screens,
    rfid_reader: RFIDReader,
    instrument: Instrument,
    lcd_flag: dict,
):
    """Display the welcome screen and wait for a card swipe."""
    await screens.welcome_screen(instrument.name)
    lcd_flag["refresh"] = False

    while True:
        card_id = await rfid_reader.read_card(timeout=20.0)
        if card_id:
            return card_id
        if lcd_flag.get("refresh", False):
            await screens.welcome_screen(instrument.name)
            lcd_flag["refresh"] = False


async def verify_user(*, card_id: str, screens: Screens):
    """Verify if the card ID corresponds to a valid user."""
    await screens.checking_user()
    user = await networking.fetch_user_data(card_id)
    if not user:
        await screens.user_not_in_database()
    await screens.user_ok(user_name=user.name)
    return user


async def start_session(
    *, user: User, instrument: Instrument, token: Token, screen: Screens
):
    """Start a recording session for the user."""
    session = await networking.start_recording(user, instrument, token)
    if not session:
        await screen.reservation_nok()
    else:
        await screen.reservation_ok()
    return session


async def display_session_info(
    screen: Screens,
    session_container: Session,
    lcd_flags: dict,
    token: Token,
):
    """Display session information continuously."""
    warning_sent = False
    while session_container.remaining_time > 0 and not session_container.ended_by_user:
        if not lcd_flags["lcd_in_use"] and session_container.remaining_time > 0:
            await networking.fetch_recording_info(token, session_container)
            # print(f"Remaining session time: {session_container.remaining_time}")
            await screen.in_session(
                remaining_session_time=session_container.remaining_time
            )
            # await asyncio.sleep(5)

            if session_container.remaining_time < 5 and warning_sent is False:
                print("Warning sent")
                await screen.session_end_warning(session_container.remaining_time)
                warning_sent = True
        await asyncio.sleep(0.5)


async def main_loop():
    """Main application loop."""

    # ---Setup
    stop_btn = Button(21)
    extend_btn = Button(13)
    lcd_controller = LCDController()
    screens = Screens(lcd_controller=lcd_controller)
    rfid_reader = RFIDReader()

    app_flags = AppFlags()
    app_context = AppContext(flags=app_flags)
    network_status = {"online": True}

    renderer = StateRenderer(screens)
    network_guard = NetworkGuard(network_status, screens, app_context)

    asyncio.create_task(
        networking.network_monitor(network_status, screens, app_context)
    )

    transition_to(app_context, AppState.INIT, renderer)
    # await renderer.render(app_context)

    # --- Token
    token: Token = await network_guard.safe_api_call(lambda: verify_token())
    if not token:
        return
    app_context.token = token

    # --- Instruments ---
    instrument: Instrument = await network_guard.safe_api_call(
        lambda: networking.fetch_instrument()
    )
    if not instrument:
        return
    app_context.instrument = instrument

    logger = Logger(instrument.mac_address, instrument.name)

    await logger.initialize()
    await logger.insert_new_row()

    await logger.write_log(1, datetime.now())
    await logger.write_log(2, instrument.ip)
    await logger.write_log(5, instrument.name)
    await logger.write_log(9, token.expiration)

    # --- Main Loop ---

    while True:
        transition_to(app_context, AppState.WAITING_FOR_CARD, renderer)

        card_id = await network_guard.safe_api_call(lambda: rfid_reader.read_card())
        if not card_id:
            continue

        user: User = await network_guard.safe_api_call(
            lambda: networking.fetch_user_data(card_id)
        )
        if not user:
            continue
        app_context.user = user

        transition_to(app_context, AppState.STARTING_SESSION, renderer)

        session: Session = await network_guard.safe_api_call(
            lambda: networking.start_recording(user, instrument, token)
        )
        if not session:
            continue
        app_context.session = session

        transition_to(app_context, AppState.IN_SESSION, renderer)

        await asyncio.gather(
            display_session_info(screens, session, app_flags, token),
            buttons_handling(
                stop_btn=stop_btn,
                extend_btn=extend_btn,
                session=session,
                screen=screens,
                token=token,
                instrument=instrument,
                user=user,
                lcd_flags=app_flags,
                network_status=network_status,
            ),
        )

        if session.ended_by_user:
            await logger.write_log(11, "Session ended by user")
        else:
            await screens.session_ended_by_timeout()
            await logger.write_log(11, "Session ended by timeout")

        app_context.session = None
        app_context.user = None
        transition_to(app_context, AppState.WAITING_FOR_CARD, renderer)

    """

    await screens.starting_screen()

    lcd_flags = {
        "lcd_in_use": False,  # False -> main is using lcd, True -> other coroutine using lcd
        "refresh": False,
    }
    input_flags = {
        "block_input": False  # False -> buttons are online, True -> buttons are offline
    }

    asyncio.create_task(
        networking.network_monitor(
            network_status=network_status,
            screens=screens,
            lcd_flags=lcd_flags,
            input_flags=input_flags,
        )
    )

    instrument: Instrument = await networking.safe_api_call(
        fetch_instrument,
        # api_func arguments
        # safe_api_call arguments
        network_status=network_status,
        api_screens=screens,
        lcd_flags=lcd_flags,
        logger=None,
    )

    while not instrument or not instrument.mac_address:
        print("Waiting for internet")

        instrument: Instrument = await networking.safe_api_call(
            fetch_instrument,
            # api_func arguments
            # safe_api_call arguments
            network_status=network_status,
            api_screens=screens,
            lcd_flags=lcd_flags,
            logger=None,
        )

    token: Token = await networking.safe_api_call(
        verify_token,
        # api_func arguments
        # safe_api_call arguments
        network_status=network_status,
        api_screens=screens,
        lcd_flags=lcd_flags,
        logger=None,
    )

    # await networking.wait_until_online(network_status, screens, lcd_flags)
    logger = Logger(instrument.mac_address, instrument.name)
    await logger.initialize()
    await logger.insert_new_row()

    await logger.write_log(1, datetime.now())
    await logger.write_log(2, instrument.ip)
    await logger.write_log(5, instrument.name)
    await logger.write_log(9, token.expiration)

    # await networking.wait_until_online(network_status, screens, lcd_flags)
    # await screens.starting_screen()

    while True:
        # await networking.wait_until_online(network_status, screens, lcd_flags)
        card_id = await networking.safe_api_call(
            welcome_and_wait_for_card,
            # api_func arguments
            screens=screens,
            rfid_reader=rfid_reader,
            instrument=instrument,
            lcd_flag=lcd_flags,
            # safe_api_call arguments
            api_screens=screens,
            network_status=network_status,
            lcd_flags=lcd_flags,
            logger=logger,
        )
        await logger.insert_new_row()
        if not card_id:
            continue

        # await networking.wait_until_online(network_status, screens, lcd_flags)
        user: User = await networking.safe_api_call(
            verify_user,
            # api_func arguments
            card_id=card_id,
            screens=screens,
            # safe_api_call arguments
            api_screens=screens,
            network_status=network_status,
            lcd_flags=lcd_flags,
            logger=logger,
        )

        if not user:
            await logger.write_log(7, card_id, datetime.now())
            continue
        else:
            # print(f"user: {user}")
            await logger.write_log(8, user.full_name, datetime.now())

        # token = await verify_token()
        # await networking.wait_until_online(network_status, screens, lcd_flags)
        session: Session = await networking.safe_api_call(
            start_session,
            # api_func arguments
            user=user,
            instrument=instrument,
            token=token,
            screen=screens,
            # safe_api_call arguments
            network_status=network_status,
            api_screens=screens,
            logger=logger,
            lcd_flags=lcd_flags,
        )
        await logger.write_log(10, datetime.now())
        if not session:
            continue

        session_container = {
            "session": session,
        }

        await asyncio.gather(
            display_session_info(
                screen=screens,
                session_container=session_container["session"],
                lcd_flags=lcd_flags,
                token=token,
            ),
            buttons_handling(
                stop_btn=stop_btn,
                extend_btn=extend_btn,
                # rfid_reader=rfid_reader,
                session=session_container["session"],
                screen=screens,
                token=token,
                instrument=instrument,
                user=user,
                lcd_flags=lcd_flags,
                network_status=network_status,
                input_flags=input_flags,
            ),
        )

        if (
            session_container["session"].ended_by_user
            or session_container["session"].remaining_time <= 0
        ):
            lcd_flags["lcd_in_use"] = True
            if session_container["session"].ended_by_user:
                await logger.write_log(11, datetime.now(), "Ended by user")
            else:
                await screens.session_ended_by_timeout()
                await logger.write_log(11, datetime.now(), "Ended by time")
    """


if __name__ == "__main__":
    asyncio.run(main_loop())
'''
