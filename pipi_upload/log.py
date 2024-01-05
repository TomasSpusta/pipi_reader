
import gspread
import config
import datetime
import LCD_display


gc = gspread.service_account(filename='/home/bluebox/pipi_reader/service_account.json')
#spredsheet_id = "1c2YquF11Lj2q4WzIapxBK5Q2SdJkwUUzT9qWL3lBwLA"

sh_name = config.mac_address

def open_sh(sh_name):
    try:
        print ("Opening SH")
        sh = gc.open(sh_name)
        print ("SH Opened")
  
    except Exception as e:
        print (e)
        print ("Creating SH")
        #if spreadsheet does not exist, create one
        sh = gc.create(sh_name)
        print ("SH Created")
        sh.share('n4norfid@gmail.com', perm_type='user', role='writer', notify=True)
        print ("SH Shared")
        sh = gc.open(sh_name)
        print ("SH Opened")
        
    ws = sh.sheet1
    if len (ws.col_values(1)) == 0:
        prepare_headers(ws)
    config.log_row = len (ws.col_values(1)) + 1
    config.sh = sh

def prepare_headers (ws):
    print ("Preparing header")
    ws.update_cell(1,1, "INTERNET CONNECTION")  #message: time stamp, note: none
    ws.update_cell(1,2, "LAN IP ADDRESS")       #message: ip address, note: timestamp
    ws.update_cell(1,3, "WLAN IP ADDRESS")      #message: ip address, note: timestamp
    ws.update_cell(1,4, "GITHUB")               #message: version, note: none
    ws.update_cell(1,5, "INSTRUMENT")           #message: instrument name, note: timestamp
    ws.update_cell(1,6, "MAIN SCRIPT")          #message: time stamp, note: none
    ws.update_cell(1,7, "CARD SWIPE")           #message: time stamp, note: card ID
    ws.update_cell(1,8, "USER INFO")            #message: time stamp, note: user name + user ID 
    ws.update_cell(1,9, "TOKEN")                #message: time stamp, note: token OK, token created, ERROR
    ws.update_cell(1,10, "RECORDING START")     #message: time stamp, note: recording OK, or NOK
    ws.update_cell(1,11, "RECORDING END")       #message: time stamp, note: recording ended by user
    print ("Headers prepared")
  
def write_log(column, log_msg, log_note=None):
    try:
        ws = config.sh.sheet1
        print('Writing to SH at columnt no.' + str (column) )
        ws.update_cell(config.log_row, column, str(log_msg))
        if log_note != None:
            note_A1_coordinates = gspread.utils.rowcol_to_a1(config.log_row, column)
            ws.update_note (note_A1_coordinates,str(log_note))
        print('Closing SH')
       # ws.client.session.close()
        
    except Exception as log_error:
        print (log_error)
        LCD_display.display ("LOG Error",str(log_error),"" ,"" ,True, True, 2)

    
'''
def makeLog (log_info):
    print (log_info)
    sh = open_sh(sheet_name)
    #sh = gc.open_by_key(spredsheet_id)
    #gc = gspread.service_account()
    
    now = datetime.datetime.now()
    
    try:
        ws = sh.worksheet(config.mac_address)
    
    except Exception as e:
        print (e)
        sh.add_worksheet(title=config.mac_address, rows=100, cols=20)
        ws = sh.worksheet(config.mac_address)
        ws.update_cell(1,1, "Time stamp" )
        ws.update_cell(1,2, "IP address" ) 
        ws.update_cell(1,3, "Equipment"  )
        ws.update_cell(1,4, "User info" )
        ws.update_cell(1,5, "User log in" )
        ws.update_cell(1,6, "User log off" )
              

    number_of_entries = len (ws.col_values(1))
    entry_row = number_of_entries + 1 
    time_col = 1
    ip_col = 2
    equip_col = 3
    user_info_col = 4
    user_in = 5
    user_off = 6
    api_crm_col = 5
    api_booking_col = 6    

    ws.update_cell(entry_row,time_col, str(now) )
    ws.update_cell(entry_row,ip_col, str(config.ip_eth0 + " " + config.ip_wlan0))
    ws.update_cell(entry_row,equip_col, config.equipment_name)
    
    
    if config.in_session == True:
        ws.update_cell(entry_row,user_info_col, (config.user_name + " " + config.user_id))
        ws.update_cell(entry_row,user_in, "Logged in")
        
    if config.logged_in and (config.in_session == False or config.ended_by_user == True):
        ws.update_cell(entry_row,user_info_col, (config.user_name + " " + config.user_id))
        ws.update_cell(entry_row,user_off, "Logged off")
    
    print('Closing SH')
    sh.client.session.close()    
'''  