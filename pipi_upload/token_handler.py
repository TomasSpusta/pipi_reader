from model_classes import Token
from datetime import datetime
from pathlib import Path
from networking import fetch_token
import json
from typing import Optional


async def initiate_token(api_key: str, TOKEN_FILE: Path) -> Optional[Token]:
    try:
        token = await fetch_token(api_key)
        await save_token(token, TOKEN_FILE)
        return token

    except Exception as e:
        print(e)


async def load_token(TOKEN_FILE: Path):
    print("Loading token...")

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as file:
            print("Token loaded.")
            data = json.load(file)
            return Token(string=data["string"], expiration=data["expiration"])


async def save_token(token: Token, TOKEN_FILE: Path):
    print("Saving token...")
    with open(TOKEN_FILE, "w") as file:
        json.dump(token.to_dict(), file)
        print("Token saved.")


async def verify_token(TOKEN_FILE: Path, api_key: str):
    print("Verifying token...")
    token = await load_token(TOKEN_FILE)

    if not token:
        print("No token found, fetching new one...")
        token = await fetch_token(api_key)
        await save_token(token, TOKEN_FILE)
        return token

    else:
        print("Token found.")
        print("Checking expiration...")
        expires_at = datetime.strptime(
            token.expiration, "%Y-%m-%dT%H:%M:%S")
        if datetime.now() >= expires_at:
            print("Token expired, refreshing...")
            token = await fetch_token(api_key)
            await save_token(token, TOKEN_FILE)
            return token
        else:
            print("Token valid.")
            return token


async def _check_expiration(token: Token) -> bool:
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

    """ if not token_data:
        
    
    if token_data is None:
        print("fetching Token")
        token = fetch_token(api_key)
        if token is not None:
            save_token(token)
            print("Saved token")
            return True
        else:
            print("Problem with get token method, check API")
            return False
    else:
        if check_expiration(token) is True:
            print("Token is OK")
            return True
        else:
            token = fetch_token(api_key)
            if token is not None:
                save_token(token)
                return True
            else:
                print("Problem with get token method, check API")
                return False """
