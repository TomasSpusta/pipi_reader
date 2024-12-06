import networking
import asyncio
from pathlib import Path
from token_handler import verify_token, initiate_token
from lcd_display_class import LCDDisplay


# TODO: ASYNCIO nastudovat, pouzit na API cally a by na seba cakali.
# https://medium.com/@moraneus/mastering-pythons-asyncio-a-practical-guide-0a673265cf04


async def main():
    lcd = LCDDisplay()
    instrument_mac_address = "e4:5f:01:ea:99:17"
    card_id = 1834257108
    API_KEY = "ude9c6nezyr71i9vf3jdtye18vwdk81s"  #
    TOKEN_FILE = Path("token_data.json")

    # token = await initiate_token(api_key, TOKEN_FILE)

    token = await verify_token(TOKEN_FILE, API_KEY)

    instrument = await networking.fetch_instrument_data(instrument_mac_address)
    user = await networking.fetch_user_data(card_id)

    if instrument:
        if user:
            if token:
                #print(f"Token: {token.string[-20:]}, Expiration: {token.expiration}")
                await networking.start_recording(user, instrument, token)
            else:
                print("Token is not OK")
        else:
            print("User is not in database - please register")
    else:
        print("Instrument-mac address pair does not exist. Check settings.")

    while True:
        # waiting screen
        await lcd.welcome_screen(instrument=instrument)

        # await the card swipe

        # validate user/reservation start
        # observe button
        # observe card swipe to elongate reservation
        # observe time to end
        # stop reservation
        # log out user
        # make log statements

        pass
        # display waiting screen


if __name__ == "__main__":
    asyncio.run(main())
