import requests
import unidecode
import aiohttp
import asyncio

from model_classes import Instrument, Token, User, Session
from screen_manager import Screens
from typing import Optional
from logger import Logger
from app_context import AppContext, AppState
from state_utils import transition_to

from getmac import get_mac_address as gma  # module for mac adress
from subprocess import check_output  # module for ip address
import config


async def check_internet_connection(timeout=3) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.google.com", timeout=timeout):
                print("Online")
                return True
    except:
        print("Offline")
        return False


async def network_monitor(
    network_status: dict,
    screens: Screens,
    app_context: AppContext,
    check_interval: float = 5.0,
):
    """
    Continuously checks internet connection.
    Updates shared state and optionally shows/hides screen warnings.
    """
    was_online = network_status.get(
        "online", True
    )  # Track previuos state to avoid screen flickering

    while True:
        is_online = await check_internet_connection()
        network_status["online"] = is_online

        if not is_online and was_online:
            # just went offline
            app_context.flags.lcd_in_use = True
            app_context.flags.block_input = True
            transition_to(app_context, AppState.OFFLINE, None)
            await screens.no_connection()
            was_online = False

        elif is_online and not was_online:
            # just came back online
            app_context.flags.lcd_in_use = False
            app_context.flags.block_input = False
            app_context.flags.screen_needs_refresh = True
            transition_to(app_context, AppState.RECOVERED, None)
            await screens.connection_restored()
            was_online = True
        await asyncio.sleep(check_interval)


async def wait_until_online(network_status: dict, screen: Screens, lcd_flags):
    while not network_status["online"]:
        lcd_flags["lcd_in_use"] = True
        await screen.no_connection()
        await asyncio.sleep(2)


async def safe_api_call(
    api_func,
    *,
    network_status: dict,
    api_screens: Screens,
    lcd_flags: dict,
    logger: Optional[Logger] = None,
    **kwargs,
):
    await wait_until_online(network_status, api_screens, lcd_flags)
    """
    Safely execute API calls and handle errors by displaying them on the LCD.
    Stops the main loop if an error occurs.

    :param api_func: The API function to execute.
    :param screens: Screens object to show errors.
    :param args: Positional arguments for the API function.
    :param kwargs: Keyword arguments for the API function.
    """
    try:
        return await api_func(**kwargs)
    except Exception as e:
        error_message = f"Error in {api_func.__name__}: {e}"
        print(error_message)

        if logger:
            await logger.write_log(12, error_message)

        await api_screens.error_message(str(e), source_function=api_func.__name__)
        return None
        # raise SystemExit("Critical Error. Stopping the program.")


async def fetch_instrument_data(mac_address: str, ip: str) -> Optional[Instrument]:
    print("Fetching instrument data")
    url = config.EQUIPMENT_BY_MAC

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"mac_address": mac_address}) as response:
                if response.status != 200:
                    print(f"Response status {response.status}")
                    error_content = await response.json()
                    print(f"Error content {error_content}")
                    error_message = error_content.get("message")
                    print(f"Message: {error_message}")
                    return None

                response_json = await response.json()
                # print(f"Response from instrument: {response_json}")

                if not response_json:
                    print("Empty response from api")
                    return None

                instrument = Instrument(
                    id=response_json[0]["equipmentid"],
                    name=response_json[0]["alias"],
                    mac_address=mac_address,
                    ip=ip,
                )
                print("Instrument's data fetched")
                return instrument

    except Exception:
        print("Error in fetch instrument")
        return None


async def fetch_user_data(card_id) -> Optional[User]:
    print("Fetching user data")
    url = config.CONTACT_BY_RFID

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"rfid": card_id}) as response:
                if response.status != 200:
                    print(f"Response status {response.status}")
                    error_content = await response.json()
                    print(f"Error content {error_content}")
                    error_message = error_content.get("message")
                    print(f"Message: {error_message}")
                    return None

                response_json = await response.json()
                # print(f"Response from user: {response_json}")

                if not response_json:
                    print("Empty response from api")
                    return None

                name = response_json[0]["firstname"]
                full_name = response_json[0]["full_name"]
                name_non_dia = unidecode.unidecode(name)
                user = User(
                    id=response_json[0]["contactid"],
                    name=name_non_dia,
                    card_id=card_id,
                    full_name=full_name,
                )
            print("User data fetched")
            return user

    except Exception:
        print("Error in fetch user")
        return None


async def start_recording(
    user: User,
    instrument: Instrument,
    token: Token,  # session: Session
) -> Optional[Session]:
    print("Initiating the recording...")
    payload = {"contactId": user.id, "equipmentId": instrument.id}
    headers = {"Authorization": "Bearer " + token.string}
    url = config.RECORDING_START
    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(
                url=url, json=payload, headers=headers
            ) as response:
                if response.status != 200:
                    error_content = await response.json()
                    error_message = error_content.get("status")
                    print(f"Message: {error_message}")
                    return None
                else:
                    response_content = await response.json()

                    print("Starting the recording...")

                    session = Session(
                        recording_id=response_content["recording"],
                        reservation_id=response_content["reservation"],
                        remaining_time=int(response_content["timetoend"]),
                    )
                    return session

    except aiohttp.ClientError:
        print("Error in start_recording")


async def stop_recording(session: Session, instrument: Instrument, token: Token):
    print("Stopping the recording...")

    payload = {
        "serviceAppointmentId": session.reservation_id,
        "equipmentId": instrument.id,
    }
    headers = {"Authorization": "Bearer " + token.string}
    url = config.RECORDING_STOP

    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(
                url=url, json=payload, headers=headers
            ) as response:
                if response.status != 200:
                    error_content = await response.json()
                    error_message = error_content.get("status")
                    print(f"Message: {error_message}")
                    return None
                else:
                    response_content = await response.json()
                    status_message = response_content.get("status")
                    print(f"Stop reservation Message: {status_message}")

    except aiohttp.ClientError:
        print("Error in stop_recording")


async def fetch_recording_info(token: Token, session: Session) -> Optional[Session]:
    headers = {"Authorization": "Bearer " + token.string}
    url = config.RECORDING_INFO.format(reservation_id=session.reservation_id)
    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(url=url, headers=headers) as response:
                if response.status != 200:
                    error_content = await response.json()
                    error_message = error_content.get("status")
                    print(f"Message: {error_message}")
                else:
                    response_content = await response.json()
                    session.remaining_time = int(response_content["timetoend"])
                    return session

    except aiohttp.ClientError:
        print("Error in fetch_recording_info")


async def fetch_token(api_key: str) -> Optional[Token]:
    url = config.FETCH_TOKEN

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"apiKey": api_key}) as response:
                if response.status != 200:
                    print(f"Response status {response.status}")
                    error_content = await response.json()
                    print(f"Error content {error_content}")
                    error_message = error_content.get("message")
                    print(f"Message: {error_message}")
                    return None

                response_json = await response.json()

                if not response_json:
                    print("Empty response from api")
                    return None

                token = Token(
                    string=response_json["accessToken"],
                    expiration=response_json["expiresAt"],
                )
                print("New token recieved")
                return token

    except Exception:
        print("Error in fetch_token")
        return None


async def fetch_mac() -> str:
    try:
        mac = gma()
        print("My MAC adress is: {}".format(mac))
        return mac

    except Exception as mac_e:
        print("Get MAC error: " + str(mac_e))


async def fetch_ip() -> str:
    try:
        ip = str(check_output(["hostname", "-I"]))

        trimmed_ip = ip[2:40]
        return trimmed_ip

    except Exception as mac_e:
        print("fetch ip error: " + str(mac_e))


async def fetch_instrument():
    """Fetch the instrument details using the MAC address."""
    ip = await fetch_ip()
    mac = await fetch_mac()
    return await fetch_instrument_data(mac, ip)
