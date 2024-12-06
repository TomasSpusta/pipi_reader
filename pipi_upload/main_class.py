import networking
import asyncio
from pathlib import Path
from token_handler import verify_token, initiate_token
from lcd_display_class import LCDDisplay
from RPLCD.i2c import CharLCD
from model_classes import Instrument
from rfid_reader_class import RFIDReader
from subprocess import check_output



# TODO: ASYNCIO nastudovat, pouzit na API cally a by na seba cakali.
# https://medium.com/@moraneus/mastering-pythons-asyncio-a-practical-guide-0a673265cf04


async def main():
    #lcd = LCDDisplay()
    ip = networking.fetch_ip
    mac = networking.fetch_mac
    lcd = CharLCD("PCF8574", 0x27)
    #instrument_mac_address = "e4:5f:01:ea:99:17"
    API_KEY = "ude9c6nezyr71i9vf3jdtye18vwdk81s"  #
    TOKEN_FILE = Path("token_data.json")
    rfid_reader = RFIDReader()
    
   #display ip address 
    #ip_address = check_output(['hostname', '-I'])
    #lcd.write_string (ip_address)
    
   
    instrument = await networking.fetch_instrument_data(mac)
        
        
    while True:
        lcd.write_string("Waiting for card....")
        card_id = await rfid_reader.read_card()
        
        if card_id:
            lcd.clear()
            lcd.write_string(f"Card ID: {card_id}")
            print(f"Card ID: {card_id}")
            await asyncio.sleep(1)
            lcd.clear()
            

                
         
            
            #GPIO.cleanup ()
    #pokus synchrnonizace
    #token = await initiate_token(api_key, TOKEN_FILE)

    #token = await verify_token(TOKEN_FILE, API_KEY)

    #instrument = await networking.fetch_instrument_data(instrument_mac_address)
    #user = await networking.fetch_user_data(card_id)
    
           
    
    
''' if instrument:
        if user:
            if token:
                pass
                #print(f"Token: {token.string[-20:]}, Expiration: {token.expiration}")
                #await networking.start_recording(user, instrument, token)
            else:
                print("Token is not OK")
        else:
            print("User is not in database - please register")
            
        #await lcd.message(line1="fsadfas",line2="afds",line3="fsadaf",line4="dfa",backlight=True,clear=True)
        #await lcd.write_string("Counter:" )
        await lcd.write("text",1)
    else:
        print("Instrument-mac address pair does not exist. Check settings.")
    '''
   
'''
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

       
        # display waiting screen
'''


if __name__ == "__main__":
    asyncio.run(main())
