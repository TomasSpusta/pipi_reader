import gspread

token_expiration = ""
token = ""
token_address = "/home/bluebox/token_data.txt"
#headers = {"Authorization" : "Bearer " + token}

#headers = {"Authorization" : "Bearer " + token}

sh : gspread.spreadsheet.Spreadsheet = ""
log_row = 0

online_status = False

mac_address = "mac address"

git_release = ""

card_id = ""

user_id = ""
user_name = ""
user_full_name = ""

equipment_id = ""
equipment_name = ""

reservation_id = ""
recording_id = ""
remaining_time = 0
files = 0
warning_sent = False

in_crm = False
recording_started = False
in_session = False
ended_by_user = False
#recording_started = ""

status_code = 0

reservation_start_time = "" 

button_pin = 40

ip_eth0 = ""
ip_wlan0 = ""




