spredsheet_id = "1c2YquF11Lj2q4WzIapxBK5Q2SdJkwUUzT9qWL3lBwLA"
import gspread

gc = gspread.service_account()

sh = gc.open_by_key(spredsheet_id)

worksheet = sh.sheet1
values = [["booooo"]]
range_name = "B2"
#worksheet.update_cell (values, range_name)
worksheet.update_cell(1, 2, 'Bingo!') #prvy radek, druhy stlpec

print(sh.sheet1.get('A1'))