
import gspread
import config

def makeLog ():
    gc = gspread.service_account(filename='/home/bluebox/service_account.json')
    spredsheet_id = "1c2YquF11Lj2q4WzIapxBK5Q2SdJkwUUzT9qWL3lBwLA"
    sh = gc.open_by_key(spredsheet_id)
    worksheet = sh.sheet1

    row = 1
    col = 2
    worksheet.update_cell(row,col, config.mac_address) #prvy radek, druhy stlpec

