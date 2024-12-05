
import networking
import json


token = networking.Token("-", "-")


def main():
    api_key = "ude9c6nezyr71i9vf3jdtye18vwdk81s"
    token_path = "token_data.txt"

    is_token_valid = networking.ApiRequests.validate_token(
        token, token_path, api_key)
    if is_token_valid is True:
        instruments = networking.ApiRequests.fetch_instruments(
            token).json()
        #print(json.dumps(instruments[0], indent=1))

        for instrument in instruments:

            print(instrument["name"] + "," + instrument["id"])


if __name__ == "__main__":
    main()
