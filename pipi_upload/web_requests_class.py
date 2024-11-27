import requests
import unidecode
from datetime import datetime


class User:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Instruemnt:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Token:
    def __init__(self, string: str, expiration: str) -> None:
        self.string = string
        self.expiration = expiration


class ApiRequests:

    @staticmethod
    def fetch_instrument_data(mac_address) -> Instruemnt or None:
        url = "https://crm.api.ceitec.cz/get-equipment-by-mac-address"
        try:
            response = requests.post(
                url, json={"mac_address": mac_address}).json()
            if len(response) == 0:

                return None

            else:

                instrument = Instruemnt(
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
    def start_recording(user_id, equipmnet_id):
        # TODO
        pass

    @staticmethod
    def check_token(token: Token) -> bool:
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
    def get_token(api_key) -> Token or None:
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
    def load_token(token: Token):
        try:
            f = open("token_data.txt", "r").readlines()
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
