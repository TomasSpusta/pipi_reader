import gspread
from gspread import Spreadsheet
from datetime import datetime
import asyncio

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
                filename="/home/bluebox/pipi_reader/service_account.json",
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
                "n4norfid@gmail.com",
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

    '''
    def open_sh():
        print("Opening SH method")
        sh_name = glob_vars.mac_address + "_" + glob_vars.equipment_name
        try:
            gc = gspread.service_account(
                filename="/home/bluebox/pipi_reader/service_account.json"
            )
            write_log_temp("gspread service: " + str(gc))
            try:
                print("Opening SH")
                sh = gc.open(sh_name)
                write_log_temp("SH opened")
                print("SH Opened")

            except Exception as sh_open_e:
                print("sh open error: " + str(sh_open_e))
                print("Creating SH")
                # if spreadsheet does not exist, create one
                sh = gc.create(sh_name)
                print("SH Created")
                write_log_temp("SH Created")
                sh.share("n4norfid@gmail.com", perm_type="user", role="writer", notify=True)
                print("SH Shared")
                sh = gc.open(sh_name)
                print("SH Opened")
                write_log_temp("SH opened")

            ws = sh.sheet1
            if len(ws.col_values(1)) == 0:
                prepare_headers(ws)
            glob_vars.log_row = len(ws.col_values(1)) + 1
            glob_vars.sh = sh
            # print (type(sh))
        except Exception as sh_open_e:
            print("Open SH LOG Error: " + str(sh_open_e))
            write_log_temp("Open SH LOG Error: " + str(sh_open_e))
            # display("LOG Error", str(sh_open_e), "", "", True, True, 2)


    def prepare_headers(ws):
        print("Preparing header")
        ws.update_cell(1, 1, "ACCESS")  # message: time stamp, note: none
        ws.update_cell(1, 2, "LAN IP ADDRESS")  # message: ip address, note: timestamp
        ws.update_cell(1, 3, "WLAN IP ADDRESS")  # message: ip address, note: timestamp
        ws.update_cell(1, 4, "GITHUB")  # message: version, note: none
        ws.update_cell(1, 5, "INSTRUMENT")  # message: instrument name, note: timestamp
        ws.update_cell(1, 6, "MAIN SCRIPT")  # message: time stamp, note: none
        ws.update_cell(1, 7, "CARD SWIPE")  # message: time stamp, note: card ID
        ws.update_cell(1, 8, "USER INFO")  # message: time stamp, note: user name + user ID
        ws.update_cell(
            1, 9, "TOKEN"
        )  # message: time stamp, note: token OK, token created, ERROR
        ws.update_cell(
            1, 10, "RECORDING START"
        )  # message: time stamp, note: recording OK, or NOK
        ws.update_cell(
            1, 11, "RECORDING END"
        )  # message: time stamp, note: recording ended by users
        print("Headers prepared")


    def write_log(column, log_msg, log_note=None):
        """
        col 1 ACCESS \n
        col 2 LAN IP \n
        col 3 WLAN IP \n
        col 4 GITHUB \n
        col 5 INSTRUMENT \n
        col 6 Main script start \n
        col 7 CARD SWIPE \n
        col 8 USER INFO \n
        col 9 TOKEN \n
        col 10 RECORDING START \n
        col 11 RECORDING END \n
        """
        try:
            # print ("marker1")
            ws = glob_vars.sh.sheet1

            print("Writing to SH at column no." + str(column))
            ws.update_cell(glob_vars.log_row, column, str(log_msg))
            if log_note != None:
                note_A1_coordinates = gspread.utils.rowcol_to_a1(glob_vars.log_row, column)
                ws.update_note(note_A1_coordinates, str(log_note))
            # print('Closing SH')
            # ws.client.session.close()

        except Exception as write_log_error:
            print("Write LOG Error: " + str(write_log_error))
            # display("LOG Error", str(write_log_error), "", "", True, True, 2)


    def write_log_temp(log_message):
        temp_log_address = "/home/bluebox/log_temp.txt"
        # temp_log_address = "pipi_upload/temp_log.txt"
        f = open(temp_log_address, "a")
        f.write(str(datetime.now()) + "\t" + log_message)
        f.write("\n")
        f.close()
    '''
