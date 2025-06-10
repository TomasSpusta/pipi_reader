from mfrc522 import SimpleMFRC522
import asyncio
import threading


class RFIDReader:
    def __init__(self) -> None:
        self.reader = SimpleMFRC522()
        self.last_card_id = None
        
    async def _read_card(self):
        try:
            print("Waiting to read card...")
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self.reader.read)
            card_id, _ = result  # Unpack the tuple to get card_id
            return card_id
        except asyncio.TimeoutError:
            print("Timeout while reading card")
            await asyncio.sleep(0.5)
            return None
        except Exception as e:
            print(f"Error in _read_card: {e}")
            return None
    
    
    
    '''    
    async def _read_card(self):
        """
        Reads a card using the RFID reader in a non-blocking way.
        Runs the blocking `read` method in an executor.
        """
        loop = asyncio.get_event_loop()
        card_id, _ = await loop.run_in_executor(None, self.reader.read)
        return card_id
    '''
    
    async def _process_card (self, card_id):
        """
        Processes the card ID, applying corrections and checking if it is new.
        """
        corrected_card_id = await self.card_id_correction(card_id)
        if corrected_card_id != self.last_card_id:
            self.last_card_id = corrected_card_id
        return str(corrected_card_id)
        
    async def read_card(self):
        """
        Waits for a card swipe and returns the processed card ID.
        """
        try:
            while True:
                await asyncio.sleep(0.1)
                card_id = await self._read_card()
                if card_id is not None:
                    return await self._process_card(card_id)
        except asyncio.CancelledError:
            print("RFID reading task was cancelled")
            raise
        except Exception as e:
            print(f"Error in read_card: {e}")
            return None
        
            
    '''
        try:
                print ("Waiting for card...")
                await asyncio.sleep(0.1)
                card_id, _ = self.reader.read()
                corrected_card_id = await self.card_id_correction(card_id)
                if corrected_card_id != self.last_card_id:
                    self.last_card_id = corrected_card_id
                return str(corrected_card_id)
                
        except asyncio.CancelledError:
                print ("RFID reading task was cancelled")
        except Exception as e:
                print(f"RFID read error: {e}")
                return None
    '''  

    async def card_id_correction(self, card_id):
        # convert decimal number from RFID reader to hexadecimal number
        hex_num = hex(card_id)
        # trim the last 2 characters from the hexadecimal number
        trimmed_hex_num = hex_num[2:10:]

        # translate the entities in hex format to the hex format from PC RFID reader
        altered_hex_num = trimmed_hex_num[6] + trimmed_hex_num[7] + trimmed_hex_num[4] + trimmed_hex_num[5] + \
            trimmed_hex_num[2] + trimmed_hex_num[3] + \
            trimmed_hex_num[0] + trimmed_hex_num[1]

        # convert altered hexadecimal number to the new decimal number, which will be the card_id sent to the API
        converted_altered_hex_num = str(int(altered_hex_num, 16))
        #print (converted_altered_hex_num)
        
        '''
        if len(converted_altered_hex_num) == 9:
            corrected_card_id = str("0" + converted_altered_hex_num)
            return corrected_card_id
        else:
            return converted_altered_hex_num
        '''     
        
        return converted_altered_hex_num.zfill(10)

    async def cleanup(self):
        self._running = False
        
    async def read_card_in_session(self):
        """
        Listens for a card swipe during a session and processes it.
        """
        try:
            print("Waiting for prolongation...")
        
            await asyncio.sleep(0.5)
            #card_id = await asyncio.wait_for (self._read_card(), timeout=5)
            card_id = await self._read_card()
            if card_id is not None:
                return await self._process_card(card_id)
        except asyncio.CancelledError:
            print("No Card present")
            #raise
            return None
        except asyncio.TimeoutError:
            print ("Timeout error")
            await asyncio.sleep(0.5)
            return None
        except Exception as e:
            print(f"Error in read_card_in_session: {e}")
            return None
        
    
    async def card_reader_time_slot(self, timeout: int):
        """
        Open a time slot to listen for card swipes.
        :param timeout: Duration of the time slot in seconds.
        :param lcd_controller: LCD controller for displaying messages.
        :return: Card ID if a card is read, None otherwise.
        """
        try:
            print(f"Listening for card swipes for {timeout} seconds...")
            card_id = await asyncio.wait_for(self.read_card(), timeout = timeout)
            
            return card_id
        
        except asyncio.TimeoutError:
            print("Time slot expired without a card swipe.")
            return None
        except asyncio.CancelledError:
            print("Card reader time slot was cancelled.")
            raise  # Propagate the cancellation
        except Exception as e:
            print(f"Error during card reader time slot: {e}")
            return None