from model_classes import Token
from datetime import datetime, timedelta
from pathlib import Path
from networking import fetch_token
import json

# from typing import Optional
import config

TOKEN_FILE = config.TOKEN_FILE
API_KEY = config.API_KEY

"""
async def initiate_token(API_KEY: str, TOKEN_FILE: Path) -> Optional[Token]:
    try:
        token = await fetch_token(API_KEY)
        await save_token(token, TOKEN_FILE)
        return token

    except Exception as e:
        print(e)
"""


async def load_token(TOKEN_FILE: Path):
    # print("Loading token...")

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as file:
            # print("Token loaded.")
            data = json.load(file)
            return Token(string=data["string"], expiration=data["expiration"])


async def save_token(token: Token, TOKEN_FILE: Path):
    # print("Saving token...")
    with open(TOKEN_FILE, "w") as file:
        json.dump(token.to_dict(), file)
        print("New token saved.")


async def verify_token():
    # print("Verifying token...")
    token = await load_token(TOKEN_FILE)

    if not token:
        # print("No token found, fetching new one...")

        token = await fetch_token(API_KEY)
        await save_token(token, TOKEN_FILE)
        return token

    else:
        # print("Token found.")
        # print("Checking expiration...")
        expires_at = datetime.strptime(token.expiration, "%Y-%m-%dT%H:%M:%S")
        if datetime.now() >= expires_at:
            print("Token expired, refreshing...")
            token = await fetch_token(API_KEY)
            await save_token(token, TOKEN_FILE)
            return token
        else:
            # print("Token valid.")
            return token


async def check_expiration(token: Token) -> bool:
    try:
        time_now_with_buffer = datetime.now() + timedelta(minutes=5)
        token_expiration_formated = datetime.fromisoformat(token.expiration)

        if token_expiration_formated < time_now_with_buffer:
            print("Token Expired")
            return False
        else:
            print(
                f"Remaining token time: {token_expiration_formated - time_now_with_buffer}"
            )
            return True

    except Exception as e:
        print("Error in checking_token: " + str(e))
        return str(e)
