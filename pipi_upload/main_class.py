import threading
import ctypes
import networking
import asyncio
from pathlib import Path
from token_handler import verify_token, initiate_token
from lcd_display_class import LCDController
from model_classes import Instrument
from rfid_reader_class import RFIDReader
from subprocess import check_output
import sys
from concurrent.futures import ThreadPoolExecutor
import signal



# TODO: ASYNCIO nastudovat, pouzit na API cally a by na seba cakali.
# https://medium.com/@moraneus/mastering-pythons-asyncio-a-practical-guide-0a673265cf04

executor = ThreadPoolExecutor()
shutdown_in_progress  =False

async def main():
    try:
        lcd_controller = LCDController()
        ip = await networking.fetch_ip()
        mac = await networking.fetch_mac()
        #instrument_mac_address = "e4:5f:01:ea:99:17"
        API_KEY = "ude9c6nezyr71i9vf3jdtye18vwdk81s"  #
        TOKEN_FILE = Path("token_data.json")
        rfid_reader = RFIDReader()  
    
        instrument = await networking.fetch_instrument_data(mac)
            
            
        while True:
            try:
                await lcd_controller.welcome_screen(instrument=instrument)
                card_id = await asyncio.wait_for(rfid_reader.read_card(),timeout=5)
                
                if card_id:
                    #lcd.clear()
                    await lcd_controller.message(line1=(f"Card ID: {card_id}"))
                    print(f"Card ID: {card_id}")
                await asyncio.sleep(1)
                    #lcd.clear()
                # Schedule both coroutines
            #lcd_task = asyncio.create_task(update_lcd())
            #button_task = asyncio.create_task(monitor_button())
            
            except asyncio.TimeoutError:
                print("Timeout while waiting for card read.")
            except asyncio.CancelledError:
                print ("Main cancelled. Cleaning up...")
                break
            except Exception as e:
                print(f"Unexpected error in main loop: {e}")
    finally:
        await rfid_reader.cleanup()
        await lcd_controller.cleanup()



def terminate_thread(thread: threading.Thread):
    """Forcefully terminate a thread."""
    if not thread.is_alive():
        return
    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc
    )
    if res == 0:
        raise ValueError("Thread not found.")
    elif res > 1:
        # If it modified more than one thread, reset and throw an error
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed.")
    print(f"Forcefully terminated thread: {thread.name}")






def log_active_threads():
    print(f"Active threads: {threading.active_count()}")
    for thread in threading.enumerate():
        print(f"Thread: {thread.name}, Alive: {thread.is_alive()}")
 
async def shutdown(loop, signal = None):
    global shutdown_in_progress
    if shutdown_in_progress:
        return
    shutdown_in_progress = True
    
    if signal:
        print (f"Recieved exit signal: {signal.name}")
    
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    
    print(f"Cancelling {len(tasks)} task(s)...")
    
    for task in tasks:
        print(f"Pending task during shutdown: {task}")
        task.cancel()
    
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(f"Error during task cancellation: {e}")
    
    print("Shutting down thread pool...")
    try:        
        executor.shutdown(wait=True)
    except Exception as e:
        print(f"Error during thread pool shutdown: {e}")
    
    print("Active threads before cleanup:")
    log_active_threads()
    
    # Forcefully stop lingering threads if still active
    for thread in threading.enumerate():
        if thread.name.startswith("asyncio") and thread.is_alive():  
            try:
                terminate_thread(thread)
            except Exception as e:
                print(f"Failed to terminate thread {thread.name}: {e}")

    print("Active threads after cleanup:")
    log_active_threads()
    
    print("Stopping event loop...")
    loop.stop()
    

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    for sig in (signal.SIGINT, signal.SIGTERM):   
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(loop, signal=s)))
    try:
        loop.run_until_complete(main())
        #asyncio.run(main())
    except KeyboardInterrupt:
        print("Ended by CTRL + C")
       
    except asyncio.CancelledError:
        print ("Program cancelled")       
          
    except Exception as e:
        print (f"Unexpected error: {e}")
           
    finally:
        print("Shutting down cleanly...")
        try:
            loop.run_until_complete(shutdown(loop))
        finally:
            loop.close()
            print("Closed")
    
            
        
        
   # Run tasks concurrently
    #await asyncio.gather(lcd_task, button_task)  

                
         
            
          
    
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