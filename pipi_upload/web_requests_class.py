import requests
import unidecode
from datetime import datetime


class User:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Instrument:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Token:
    def __init__(self, string: str, expiration: str):
        self.string = string
        self.expiration = expiration


class ApiRequests:

    @staticmethod
    def fetch_instrument_data(mac_address) -> Instrument or None:
        url = "https://crm.api.ceitec.cz/get-equipment-by-mac-address"
        try:
            response = requests.post(
                url, json={"mac_address": mac_address}).json()
            if len(response) == 0:

                return None

            else:

                instrument = Instrument(
                    id=response[0]["equipmentid"],
                    name=response[0]["alias"]
                )
                return instrument

        except Exception as e:
            print("Error in fetch_instruemnt_data: " + str(e))
            return str(e)

    @staticmethod
    def fetch_user_data(card_id) -> User or None:
        url = "https://crm.api.ceitec.cz/get-contact-by-rfid"
        try:
            user_data = requests.post(url, json={"rfid": card_id}).json()
            if len(user_data) == 0:
                note = "User do not have card in CRM - register card"
                return None

            else:
                name = user_data[0]["firstname"]
                name_non_dia = unidecode.unidecode(name)
                user = User(
                    id=user_data[0]["contactid"],
                    name=name_non_dia
                )
                return user

        except Exception as e:
            print("Error in fetch_user_data: " + str(e))
            return str(e)

    @staticmethod
    def start_recording(user: User, instrument: Instrument, token: Token):
        payload = {"contactId": user.id, "equipmentId": instrument.id}
        headers = {"Authorization": "Bearer " + token.string}
        url = "https://booking.ceitec.cz/api/recording/start/"
        try:
            response = requests.post(url=url, json=payload, headers=headers)
            print(response)
            return response

        except requests.exceptions.RequestException as e:
            print("Error in start_recording: " + e)

    @staticmethod
    def validate_recording(recording_response: requests.Response) -> bool:
        if recording_response.status_code == 200:
            return True
        elif recording_response.status_code == 400 or 404 or 500:
            return False
        else:
            return False

    @staticmethod
    def fetch_instruments(token: Token):
        headers = {"Authorization": "Bearer " + token.string}
        params = {
            "filters[]": ["ge_corefacilityid:eq:ea950b30-5f22-eb11-80cb-005056914121"],
        }
        try:
            response = requests.get(
                "https://booking.ceitec.cz/api/equipment", headers=headers, params=params)
            '''
                params = {
                    "filters[]": ["Robert", "2024-11-01", "2024-11-30"],  # Replace start and end values with actual dates
                    "scope": "activity_parties.partyid"
                }
            '''
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    @staticmethod
    def check_expiration(token: Token) -> bool:
        try:
            time_now = datetime.now().isoformat(timespec="seconds")
            time_now_formated = datetime.strptime(
                time_now, "%Y-%m-%dT%H:%M:%S")
            token_expiration_formated = datetime.strptime(
                token.expiration, "%Y-%m-%dT%H:%M:%S")

            if token_expiration_formated < time_now_formated:
                return False
            else:
                return True

        except Exception as e:
            print("Error in checking_token: " + str(e))
            return str(e)

    @staticmethod
    def fetch_token(api_key) -> Token or None:
        try:
            api_key = api_key
            url = "https://booking.ceitec.cz/api/login"
           # user_data = requests.post(url, json={"rfid": card_id}).json()
            response = requests.post(url, json={"apiKey": api_key}).json()

            if len(response) == 0:
                return None

            else:
                token = Token(
                    string=response["accessToken"],
                    expiration=response["expiresAt"]
                )
            return token

        except Exception as e:
            print("Error in get_token: " + str(e))
            return None

    @staticmethod
    def load_token(token: Token, token_path: str):
        try:
            f = open(token_path, "r").readlines()
            token.expiration = f[0][:-1]
            token.string = f[1]
            print("load token completed")
            return token

        except Exception as e:
            print("Error in load_token: " + str(e))
            return None

    @staticmethod
    def save_token(token: Token):
        try:
            token_directory = "token_data.txt"
            f = open(token_directory, "w")
            f.writelines([token.expiration + "\n", token.string])
            f.close()
        except Exception as e:
            print("Error in save_token: " + str(e))
            return None

    @staticmethod
    def validate_token(token: Token, token_path: str, api_key: str, ) -> bool:
        # try to load token
        loaded_token = ApiRequests.load_token(token, token_path)
        if loaded_token is None:
            print("fetching Token")
            token = ApiRequests.fetch_token(api_key)
            if token != None:
                ApiRequests.save_token(token)
                print("Token is OK")
                return True
            else:
                print("Problem with get token method, check API")
                return False
        else:
            if ApiRequests.check_expiration(token) is True:
                print("Token is OK")
                return True
            else:
                token = ApiRequests.fetch_token(api_key)
                if token != None:
                    ApiRequests.save_token(token)
                    return True
                else:
                    print("Problem with get token method, check API")
                    return False
