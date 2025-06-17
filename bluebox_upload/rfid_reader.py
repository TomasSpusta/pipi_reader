from mfrc522 import SimpleMFRC522
import asyncio


class RFIDReader:
    def __init__(self) -> None:
        self.reader = SimpleMFRC522()
        self.last_card_id = None

    """
    async def _read_card(self):
        try:
            # print("Waiting to read card...")
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
    """

    async def _process_card(self, card_id: int) -> str:
        """
        Processes the card ID, applying corrections and checking if it is new.
        """
        corrected_card_id = await self.card_id_correction(card_id)
        if corrected_card_id != self.last_card_id:
            self.last_card_id = corrected_card_id
        return str(corrected_card_id)

    async def read_card(self, timeout: float = 10.0) -> str | None:
        """
        Waits for a card swipe and returns the processed card ID.
        Timeouts periaodically to refresh lcd display
        """
        try:
            loop = asyncio.get_event_loop()

            card_id = await asyncio.wait_for(
                loop.run_in_executor(None, self.reader.read), timeout=timeout
            )
            if card_id:
                card_id, _ = card_id
                return await self._process_card(card_id)
            return None
        except asyncio.TimeoutError:
            print("RFID reader timeout")
            return None
        except asyncio.CancelledError:
            print("RFID reading task was cancelled")
            raise
        except Exception as e:
            print(f"Error in read_card: {e}")
            return None

    async def card_id_correction(self, card_id: int) -> str:
        # convert decimal number from RFID reader to hexadecimal number
        hex_num = hex(card_id)[2:].zfill(
            8
        )  # Convert to hex, strip '0x', pad to 8 chars
        reversed_hex = (
            hex_num[6:8]
            + hex_num[4:6]
            + hex_num[2:4]
            + hex_num[0:2]  # Reverse byte order
        )
        corrected = str(int(reversed_hex, 16)).zfill(
            10
        )  # Convert back to int and zero-pad
        return corrected
