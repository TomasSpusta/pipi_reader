import gspread
import glob_vars
from lcd_display import display


# spredsheet_id = "1c2YquF11Lj2q4WzIapxBK5Q2SdJkwUUzT9qWL3lBwLA"

# sh_name = config.mac_address


def open_sh(sh_name):
    try:
        gc = gspread.service_account(filename="/home/bluebox/pipi_reader/service_account.json")
        try:
            print("Opening SH")
            sh = gc.open(sh_name)
            print("SH Opened")

        except Exception as sh_open_e:
            print("sh open error: " + str(sh_open_e))
            print("Creating SH")
            # if spreadsheet does not exist, create one
            sh = gc.create(sh_name)
            print("SH Created")
            sh.share("n4norfid@gmail.com", perm_type="user", role="writer", notify=True)
            print("SH Shared")
            sh = gc.open(sh_name)
            print("SH Opened")

        ws = sh.sheet1
        if len(ws.col_values(1)) == 0:
            prepare_headers(ws)
        glob_vars.log_row = len(ws.col_values(1)) + 1
        glob_vars.sh = sh
        #print (type(sh))
    except Exception as sh_open_e:
        print("Open SH LOG Error: " + str(sh_open_e))
        display("LOG Error", str(sh_open_e), "", "", True, True, 2)


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
    ws.update_cell(1, 9, "TOKEN")  # message: time stamp, note: token OK, token created, ERROR
    ws.update_cell(1, 10, "RECORDING START")  # message: time stamp, note: recording OK, or NOK
    ws.update_cell(1, 11, "RECORDING END")  # message: time stamp, note: recording ended by users
    print("Headers prepared")


def write_log(column, log_msg, log_note=None):
    """
    col 1 ACCESS \n
    col 2 LAN IP \n
    col 3 WLAN IP \n
    col 4 GITHUB \n
    col 5 MAC address \n
    col 6 Main script start \n
    col 7 CARD SWIPE \n
    col 8 USER INFO \n
    col 9 TOKEN \n
    """
    try:
        ws = glob_vars.sh.sheet1
        
        print("Writing to SH at column no." + str(column))
        ws.update_cell(glob_vars.log_row, column, str(log_msg))
        if log_note != None:
            note_A1_coordinates = gspread.utils.rowcol_to_a1(glob_vars.log_row, column)
            ws.update_note(note_A1_coordinates, str(log_note))
        # print('Closing SH')
        #ws.client.session.close()
    

    except Exception as write_log_error:
        print("Write LOG Error: " + str(write_log_error))
        display("LOG Error", str(write_log_error), "", "", True, True, 2)

