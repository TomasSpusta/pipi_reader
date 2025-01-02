
import networking
import asyncio
from pathlib import Path
from token_handler import verify_token, initiate_token
from lcd_display_class import LCDController
from model_classes import Instrument, Session
from rfid_reader_class import RFIDReader
from gpiozero import Button



# TODO: ASYNCIO nastudovat, pouzit na API cally a by na seba cakali.
# https://medium.com/@moraneus/mastering-pythons-asyncio-a-practical-guide-0a673265cf04

async def main():
    
    try:
        button = Button(21)
        lcd_controller = LCDController()
        rfid_reader = RFIDReader()
        #session = Session()  
        ip = await networking.fetch_ip()
        mac = await networking.fetch_mac()
        #instrument_mac_address = "e4:5f:01:ea:99:17"
        API_KEY = "ude9c6nezyr71i9vf3jdtye18vwdk81s"  #
        TOKEN_FILE = Path("token_data.json")
        
        token = await verify_token(TOKEN_FILE, API_KEY) 
        #token = await initiate_token(API_KEY, TOKEN_FILE)
        instrument = await networking.fetch_instrument_data(mac)
        
        
            
            
        while True:
            
            try:
                if instrument:
                    await lcd_controller.welcome_screen(instrument=instrument)
                    card_id = await asyncio.wait_for(rfid_reader.read_card(),timeout=5)
                    print (card_id)
                    if card_id:
                        user = await networking.fetch_user_data(card_id)
                        print (f"User name: {user.name}")
                        if user:
                            token = await verify_token(TOKEN_FILE, API_KEY)
                            session = await networking.start_recording(user, instrument, token, session=None)
                            if session:
                                await lcd_controller.message("Recording is running")
                                
                                while session.remaining_time > 0:
                                    print (f"session loop... remaining time {session.remaining_time} ")
                                    async with asyncio.TaskGroup() as tg:
                                        task1 = tg. create_task (lcd_controller.write (text = f"Remaing session time{session.remaining_time} minutes", row=2))
                                        task2 = tg. create_task (monitor_button(button, lcd_controller))
                                        task3 = tg. create_task (networking.fetch_reservation_info (token, session))
                                    #print (f"Session data in main loop:\n{session}")
                                    
                 #                   print ("Fetching reservation info")
                                    #session = await networking.fetch_reservation_info (token, session)
                                  
                                    #print (f"Session data in main loop:\n{session}")
                                    
                                  
                #                    print ("Showing remaining time")
                                   
                                                  
                                    print ("Gathering tasks")
                                    await asyncio.gather(task1, task2, task3)
                                    print ("Sleep 5 sec")
                                    await asyncio.sleep (5)
                                    
                                    
                                else:
                                    print (f"Session ended")
                                    await lcd_controller.message(line1="Recording is ended", display_time=5)
                            
                            #print (recording_message)
                            #TODO: Dodelat logiku prihlasovani.
                        
                await asyncio.sleep(0.2)       
                       
            except asyncio.TimeoutError:
                print("Timeout while waiting for card read.")
            except asyncio.CancelledError:
                print ("Main cancelled. Cleaning up...")
                break
            except Exception as e:
                print(f"Unexpected error in main loop: {e}")
    finally:
        print ("Finally block")
        await rfid_reader.cleanup()
        await lcd_controller.cleanup()


async def monitor_button(button:Button, lcd_controller: LCDController):
    """Coroutine to handle button presses."""
    hold_time = 0
    while True:
        if button.is_pressed:
            print ("Button pressed")
                         
            hold_time += 1
            if hold_time >= 3:
                print ("Button held")
                await lcd_controller.clear()
                await lcd_controller.message("Session ended by user")
                await asyncio.sleep(0.5)  # Debounce delay
                hold_time = 0
                
        else:
            hold_time = 0
            #break
        #print ("Button is not pressed")
        await asyncio.sleep(0.5) # Check button status frequently
        
        
  



    

if __name__ == "__main__":
    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Ended by CTRL + C")
       
    except asyncio.CancelledError:
        print ("Program cancelled")       
          
    except Exception as e:
        print (f"Unexpected error: {e}")
           
   
 
    
    
           
    
    
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