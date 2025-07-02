from rfid_reader import RFIDReader
import asyncio


async def main():
    rfid_reader = RFIDReader()
    card_id = await rfid_reader.read_card()
    print(card_id)


if __name__ == "__main__":
    asyncio.run(main())
