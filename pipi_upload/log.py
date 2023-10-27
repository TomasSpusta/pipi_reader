
import gspread
import config
import datetime


def makeLog ():
    gc = gspread.service_account(filename='/home/bluebox/service_account.json')
    #gc = gspread.service_account()
    spredsheet_id = "1c2YquF11Lj2q4WzIapxBK5Q2SdJkwUUzT9qWL3lBwLA"
    sh = gc.open_by_key(spredsheet_id)
    '''
    potom dodelat, ze kdyz neni mac adresa v seznamu, tak udela novy worksheet s mac artesou, udela hlavicku a tak
    '''
    
    ws = sh.worksheet(config.mac_address)

    #worksheet = sh.sheet1
    now = datetime.datetime.now()

    number_of_entries = len (ws.col_values(1))
    entry_row = number_of_entries + 1 
    time_col = 1
    ip_col = 2
    equip_col = 3
    user_col = 4
    api_crm_col = 5
    api_booking_col = 6

   
    ws.update_cell(entry_row,time_col, str(now) )
    ws.update_cell(entry_row,ip_col, str(config.ip_eth0 + " " + config.ip_wlan0))
    ws.update_cell(entry_row,equip_col,config.equipment_name)
    #ws.update_cell(entry_row,user_col, (config.user_name + " " + config.user_id))
    

    
    
    
    
    
    
    
    
    
    
