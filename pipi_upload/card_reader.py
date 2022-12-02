from mfrc522 import SimpleMFRC522
import config

#create RFID reader instance
reader = SimpleMFRC522() 

#Function dealing with sending and recieving the data.
#Parameter rfid is card number from MFRC522 reader

def card_reader():
    RFID_id, text = reader.read()
    #print ('Readed card: ' + str(rfid)) 
    
    # convert decimal number from RFID reader to hexadecimal number
    hex_num = hex (RFID_id)
    # trim the last 2 characters from the hexadecimal
    trimmed_hex_num = hex_num [2:10:]
    print (trimmed_hex_num)
    
    altered_hex_num = trimmed_hex_num [6] + trimmed_hex_num [7] + trimmed_hex_num [4] + trimmed_hex_num [5] + trimmed_hex_num [2] + trimmed_hex_num [3] + trimmed_hex_num [0] + trimmed_hex_num [1]
    
    print (altered_hex_num)
    
    new_dec_num = int (altered_hex_num,16)
    print (new_dec_num)