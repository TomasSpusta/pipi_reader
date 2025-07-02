from mfrc522 import SimpleMFRC522
import asyncio
import time


class RFIDReader:
    def __init__(self) -> None:
        self.reader = SimpleMFRC522()
        self.last_card_id = None
        self._last_read_time = 0
        self._cooldown = 2

    async def read_card(self) -> str | None:
        try:
            card_id, _ = self.reader.read()
            now = time.time()

            if (
                card_id != self.last_card_id
                or (now - self._last_read_time) > self._cooldown
            ):
                self._last_read_time = now
                self.last_card_id = card_id
                return await self._process_card(card_id)
            return None
        except Exception as e:
            print(f"RFID read error: {e}")
            return None

    async def _process_card(self, card_id: int) -> str:
        """
        Processes the card ID, applying corrections and checking if it is new.
        """
        corrected_card_id = await self.card_id_correction(card_id)
        return str(corrected_card_id)

    async def card_id_correction(self, card_id: int) -> str:
        # convert decimal number from RFID reader to hexadecimal number
        # Convert to hex, strip '0x', pad to 8 chars
        hex_num = hex(card_id)[2:].zfill(8)
        # Reverse byte order
        reversed_hex = hex_num[6:8] + hex_num[4:6] + hex_num[2:4] + hex_num[0:2]
        # Convert back to int and zero-pad
        corrected = str(int(reversed_hex, 16)).zfill(10)
        # print(corrected)
        return corrected

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def clear_queue(self):
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
                self.queue.task_done()
            except asyncio.QueueEmpty:
                break

    """
    async def _poll_cards(self):
        print("Polling started")
        loop = asyncio.get_event_loop()
        while True:
            try:
                card_id, _ = await loop.run_in_executor(None, self.reader.read)
                now = time.time()
                # await self.queue.put(processed_id)
                print(f"Queue size: {self.queue.qsize()}")
                # print(f"Processed card from _poll_cards -> {processed_id}")

                if (
                    card_id != self.last_card_id
                    or (now - self._last_read_time) > self._cooldown
                ):
                    self._last_read_time = now
                    self.last_card_id = card_id

                    processed_id = await self._process_card(card_id)
                    await self.queue.put(processed_id)
                else:
                    print("duplicare card id ignored")
                print(f"Queue size: {self.queue.qsize()}")
                await asyncio.sleep(0.5)

            except Exception as e:
                print(f"RFID reader error:{e}")
                await asyncio.sleep(1)
   
    async def get_card(self, timeout: float = 30.0) -> str | None:
        print(f"Get_card Reader instance id: {id(self)}")
        try:
            print("Calling get_card()...")
            card = await asyncio.wait_for(self.queue.get(), timeout)
            await asyncio.sleep(0.1)
            print(f"get_card card -> {card}")
            return card
        except asyncio.TimeoutError:
            return None
    """
