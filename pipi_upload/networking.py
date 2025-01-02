import requests
import unidecode
import aiohttp

from model_classes import Instrument, Token, User, Session
from typing import Optional

from getmac import get_mac_address as gma  # module for mac adress
from subprocess import check_output #module for ip address


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


async def start_recording(user: User, instrument: Instrument, token: Token, session:Session) -> Optional[ Session]:
    print("Starting the recording...")
    payload = {"contactId": user.id, "equipmentId": instrument.id}
    headers = {"Authorization": "Bearer " + token.string}
    url = "https://booking.ceitec.cz/api/recording/start/"
    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(url=url, json=payload, headers=headers) as response:

                if response.status != 200:
                    error_content = await response.json()
                    #print(f"Error content {error_content}")
                    error_message = error_content.get("status")
                    print(f"Message: {error_message}")
                    return None
                else:
                    response_content = await response.json()
                    #print(f"response content {response_content}")
                    status_message = response_content.get("status")
                    print(f"Message: {status_message}")
                    
                    session = Session(
                        recording_id = response_content["recording"],
                        reservation_id= response_content["reservation"] ,
                        remaining_time= int(response_content["timetoend"]) 
                    )
                    #print (f"Session data in networking:\n{session}")
                    return session
                    
                    

    except aiohttp.ClientError as e:
        print("Error in start_recording: " + e)

async def fetch_reservation_info (token:Token, session:Session) -> Optional[ Session]:
    print("Fetching recording info...")
    headers = {"Authorization": "Bearer " + token.string}
    url = f"https://booking.ceitec.cz/api/service-appointment/{session.reservation_id}/raspberry"
    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(url=url, headers=headers) as response:
                print (f"Response status recording info:{response.status}")
                if response.status != 200:
                    error_content = await response.json()
                    #print(f"Error content {error_content}")
                    error_message = error_content.get("status")
                    print(f"Message: {error_message}")
                    #return None
                else:
                    
                    response_content = await response.json()
                    #print(f"response content {response_content}")
                    
                    session.remaining_time= int(response_content["timetoend"]) 
                    
                    
                    return session
                    

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


             
async def fetch_mac () -> str:
        try:
            mac = gma()  
            print("My MAC adress is: {}".format(mac))
            return mac

        except Exception as mac_e:
            print("Get MAC error: " + str(mac_e))
            
async def fetch_ip () -> str:
        try:
            ip = check_output(['hostname', '-I'])
            print("My IP adress is: {}".format(ip))
            return ip

        except Exception as mac_e:
            print("fetch ip error: " + str(mac_e))