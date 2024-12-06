import requests
import unidecode
import aiohttp

from model_classes import Instrument, Token, User
from typing import Optional


async def fetch_instrument_data(mac_address:str) -> Optional[Instrument]:
    print("Fetching instrument data")
    url = "https://crm.api.ceitec.cz/get-equipment-by-mac-address"

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
                #print(f"Response from instrument: {response_json}")

                if not response_json:
                    print("Empty response from api")
                    return None

                instrument = Instrument(
                    id=response_json[0]["equipmentid"],
                    name=response_json[0]["alias"]
                )
                print("Instrument's data fetched")
                return instrument

    except Exception as e:
        print(f"Error in fetch instrument: {e}")
        return None


async def fetch_user_data(card_id) -> Optional[User]:
    print("Fetching user data")
    url = "https://crm.api.ceitec.cz/get-contact-by-rfid"

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
                #print(f"Response from user: {response_json}")

                if not response_json:
                    print("Empty response from api")
                    return None

                name = response_json[0]["firstname"]
                name_non_dia = unidecode.unidecode(name)
                user = User(
                    id=response_json[0]["contactid"],
                    name=name_non_dia
                )
            print("User data fetched")
            return user

    except Exception as e:
        print(f"Error in fetch user: {e}")
        return None


async def start_recording(user: User, instrument: Instrument, token: Token):
    print("Starting the recording...")
    payload = {"contactId": user.id, "equipmentId": instrument.id}
    headers = {"Authorization": "Bearer " + token.string}
    url = "https://booking.ceitec.cz/api/recording/start/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=payload, headers=headers) as response:

                if response.status != 200:
                    error_content = await response.json()
                    #print(f"Error content {error_content}")
                    error_message = error_content.get("status")
                    print(f"Message: {error_message}")
                    return None
                else:
                    error_content = await response.json()
                    #print(f"Error content {error_content}")
                    error_message = error_content.get("status")
                    print(f"Message: {error_message}")
                    return None

    except aiohttp.ClientError as e:
        print("Error in start_recording: " + e)


async def fetch_instruments(token: Token):
    headers = {"Authorization": "Bearer " + token.string}
    params = {
        "filters[]": ["ge_corefacilityid:eq:ea950b30-5f22-eb11-80cb-005056914121"],
    }
    try:
        response = requests.get(
            "https://booking.ceitec.cz/api/equipment", headers=headers, params=params)
        '''
                params = {
                    "filters[]": ["Robert", "2024-11-01", "2024-11-30"],  
                    "scope": "activity_parties.partyid"
                }
            '''
        return response
    except requests.exceptions.RequestException as e:
        print(e)


async def fetch_token(api_key: str) -> Optional[Token]:
    url = "https://booking.ceitec.cz/api/login"

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
                    expiration=response_json["expiresAt"]
                )
                print("New token recieved")
                return token

    except Exception as e:
        print(f"Error in fetch token: {e}")
        return None
