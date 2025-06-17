import gspread
from gspread import Spreadsheet
from datetime import datetime
import asyncio
import config

import gspread.utils

# spredsheet_id = "1c2YquF11Lj2q4WzIapxBK5Q2SdJkwUUzT9qWL3lBwLA"

# sh_name = config.mac_address


class Logger:
    def __init__(self, mac_address, equipment_name):
        self.sh_name = f"{mac_address}_{equipment_name}"
        self.gc = None
        self.sheet: Spreadsheet = None
        self.current_log_row = 2  # <- this has to be tested, so logs are writen in row 2 and do not erase previous logs

    async def initialize(self):
        try:
            self.gc = await asyncio.to_thread(
                gspread.service_account,
                filename=config.LOGGER_JSON,
            )
            self.sheet = await self._open_or_create_sheet()

        except Exception as e:
            print(f"Error initialize logger: {e}")
            await self.write_local_log(f"Error initialize logger: {e}")

    async def _open_or_create_sheet(self):
        try:
            print("Sheet found - Opening sheet...")
            sheet = await asyncio.to_thread(self.gc.open, self.sh_name)

        except gspread.SpreadsheetNotFound as e:
            print(f"Error in open_or_create_sheet: {e}")
            print("Sheet not existing - Creating sheet...")
            # except Exception as e:
            sheet = await asyncio.to_thread(self.gc.create, self.sh_name)
            print("Sharing sheet...")
            await asyncio.to_thread(
                sheet.share,
                config.LOGGER_ACC,
                perm_type="user",
                role="writer",
                notify=True,
            )
            print("Preapring headers...")
            await self._prepare_headers(sheet.sheet1)

        except Exception as e:
            print(f"Error in _open_or_create_sheet: {e}")
            await self.write_local_log(f"Error in _open_or_create_sheet: {e}")

        return sheet.sheet1

    async def _prepare_headers(self, ws):
        headers = [
            "BOOT UP",
            "LAN IP",
            "WLAN IP",
            "GITHUB BRANCH",
            "INSTRUMENT",
            "MAIN SCRIPT",
            "CARD SWIPE",
            "USER INFO",
            "TOKEN",
            "RECORDING START",
            "RECORDING END",
            "ERROR",
        ]
        for idx, header in enumerate(headers, start=1):
            ws.update_cell(1, idx, header)

    async def insert_new_row(self):
        """Insert a new row below the headers for a new card swipe."""
        try:
            if not self.sheet:
                raise Exception("Google sheet not initialized")

            await asyncio.to_thread(self.sheet.insert_row, [], 2)
            self.current_log_row = 2
        except Exception as e:
            await self.write_temp_log(f"Error inserting new log row: {str(e)}")

    async def write_log(self, column, log_msg, log_note=None):
        """1 ACCESS,  2 LAN IP,  3 WLAN IP \n
        4 GITHUB BRANCH
        5 INSTRUMENT
        6 Main script start \n
        7 CARD SWIPE
        8 USER INFO
        9 TOKEN \n
        10 RECORDING START
        11 RECORDING END
        12 ERROR"""
        try:
            if not self.sheet:
                raise Exception("Google sheet not initialized")

            print(f"Writing log in column {column}")
            await asyncio.to_thread(
                self.sheet.update_cell, self.current_log_row, column, str(log_msg)
            )

            if log_note:
                note_cell = gspread.utils.rowcol_to_a1(self.current_log_row, column)
                await asyncio.to_thread(
                    self.sheet.update_note, note_cell, str(log_note)
                )
        except Exception as e:
            print(f"Error in write log: {e}")
            await self.write_local_log(f"Error in write log: {str(e)}")

    async def write_local_log(self, message):
        with open("/home/bluebox/log_local.txt", "a") as f:
            f.write(f"{datetime.now()} - {message}\n")
            f.close()
