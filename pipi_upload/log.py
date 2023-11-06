
import gspread
import config
import datetime


gc = gspread.service_account(filename='/home/bluebox/service_account.json')
spredsheet_id = "1c2YquF11Lj2q4WzIapxBK5Q2SdJkwUUzT9qWL3lBwLA"


def makeLog (log_info):
    print (log_info)
    sh = gc.open_by_key(spredsheet_id)
    #gc = gspread.service_account()
    
    now = datetime.datetime.now()
    
    try:
        ws = sh.worksheet(config.mac_address)
    
    except Exception as e:
        #print (e)
        sh.add_worksheet(title=config.mac_address, rows=100, cols=20)
        ws = sh.worksheet(config.mac_address)
        ws.update_cell(1,1, "Time stamp" )
        ws.update_cell(1,2, "IP address" ) 
        ws.update_cell(1,3, "Equipment"  )
        ws.update_cell(1,4, "User info" )
        ws.update_cell(1,5, "User log in" )
        ws.update_cell(1,6, "User self log off" )
              

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
    
    
    if config.logged_in == True:
        ws.update_cell(entry_row,user_info_col, (config.user_name + " " + config.user_id))
        ws.update_cell(entry_row,user_in, "Logged in")
        
    if config.in_session == False or config.ended_by_user == True:
        ws.update_cell(entry_row,user_off, "Logged off")
        
  
    

    
    
    
    
    
    
    
    
    
    
