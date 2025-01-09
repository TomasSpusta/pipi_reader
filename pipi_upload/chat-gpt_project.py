import asyncio
from state_machine import StateMachine
from screens import Screens
from model_classes import Instrument
from lcd_controller import LCDController
from networking import fetch_instrument_data, fetch_mac, fetch_user_data
from token_handler import verify_token
from program_context import ProgramStateContext
from rfid_reader_class import RFIDReader
from button_handler_ai import ButtonHandler
import keys


async def fetch_instrument(state_context):
    try:
        mac_address = await fetch_mac()
        if mac_address:
            fetched_instrument = await fetch_instrument_data(mac_address)
            if fetched_instrument:
                state_context.instrument = Instrument(
                    id=fetched_instrument["id"],
                    name=fetched_instrument["name"],
                    mac_address=mac_address,
                )
            else:
                print("Failed to fetch instrument data, setting default values.")
                state_context.instrument = Instrument(
                    id="unknown", name="Unknown Instrument", mac_address=mac_address
                )
        else:
            print("Failed to fetch MAC address, setting default values.")
            state_context.instrument = Instrument(
                id="unknown", name="Unknown Instrument", mac_address=None
            )
    except Exception as e:
        print(f"Error fetching instrument data: {e}")
        state_context.instrument = Instrument(
            id="unknown", name="Unknown Instrument", mac_address=None
        )


async def fetch_token(state_context, lcd_controller):
    try:
        await lcd_controller.message(Screens.CHECKING_TOKEN)
        token = await verify_token(keys.TOKEN_FILE, keys.API_KEY)
        if token:
            state_context.token.string = token.string
            state_context.token.expiration = token.expiration
            print("Token validated successfully.")

        else:
            print("Token validation failed.")

    except Exception as e:
        print(f"Error checking token: {e}")


async def update_lcd(state_machine, state_context, lcd_controller):
    previous_state = None
    previous_message = ""
    while True:
        if state_machine.state != previous_state:
            if state_machine.state == "waiting":
                message = "\n".join(
                    [
                        line.format(instrument_name=state_context.instrument.name)
                        for line in Screens.WELCOME
                    ]
                )
            elif state_machine.state == "user_ok":
                message = "\n".join(
                    [
                        line.format(
                            user_name=state_context.user.name,
                            random_phrase=state_context.random_phrase,
                        )
                        for line in Screens.USER_OK
                    ]
                )
            else:
                screen_mapping = {
                    "checking_user": Screens.CHECKING_USER,
                    "checking_token": Screens.CHECKING_TOKEN,
                    "user_nok": Screens.USER_NOK,
                    "checking_reservation": Screens.CHECKING_RESERVATION,
                    "reservation_ok": Screens.RESERVATION_OK,
                    "reservation_nok": Screens.RESERVATION_NOK,
                    "reservation_prolonged": Screens.RESERVATION_PROLONGED,
                    "session_ended_by_user": Screens.SESSION_ENDED_BY_USER,
                    "session_ended": Screens.SESSION_ENDED,
                }
                lines = screen_mapping.get(state_machine.state, ["Unknown State"])
                message = "\n".join(lines)

            if message != previous_message:  # Only update if the message changes
                await lcd_controller.message(message)
                previous_message = message

            previous_state = state_machine.state

        await asyncio.sleep(0.1)


async def card_reader_handler(state_machine, state_context, card_reader):
    while True:
        if state_machine.state == "waiting":
            card_id = await card_reader.read_card()
            if card_id:
                state_machine.start_session()
                fetched_user = await fetch_user_data(card_id)
                if fetched_user:
                    state_context.user.id = fetched_user["id"]
                    state_context.user.name = fetched_user["name"]
                    state_machine.validate_user()
                else:
                    state_machine.invalidate_user()
        await asyncio.sleep(0.1)


def button_pressed(state_machine):
    match state_machine.state:
        case "checking_reservation":
            state_machine.confirm_reservation()
        case "in_session":
            state_machine.end_session_by_user()
        case "loading":
            state_machine.end_session()


async def main():
    state_machine = StateMachine()
    state_context = ProgramStateContext()
    lcd_controller = LCDController()
    card_reader = RFIDReader()
    button_handler = ButtonHandler()

    button_handler.set_callback(lambda: button_pressed(state_machine))

    await fetch_instrument(state_context)
    await fetch_token(state_context, lcd_controller)

    tasks = [
        update_lcd(state_machine, state_context, lcd_controller),
        card_reader_handler(state_machine, state_context, card_reader),
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated.")
