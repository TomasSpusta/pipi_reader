from mfrc522 import SimpleMFRC522
import glob_vars

#create RFID reader instance
reader = SimpleMFRC522() 

#Function dealing with sending and recieving the data.
#Parameter rfid is card number from MFRC522 reader

def card_reader():
    RFID_id, text = reader.read()
    #print ('Readed card: ' + str(RFID_id)) 
    
    # convert decimal number from RFID reader to hexadecimal number
    hex_num = hex (RFID_id)
    # trim the last 2 characters from the hexadecimal number
    trimmed_hex_num = hex_num [2:10:]
       
    # translate the entities in hex format to the hex format from PC RFID reader
    altered_hex_num = trimmed_hex_num [6] + trimmed_hex_num [7] + trimmed_hex_num [4] + trimmed_hex_num [5] + trimmed_hex_num [2] + trimmed_hex_num [3] + trimmed_hex_num [0] + trimmed_hex_num [1]
       
    # convert altered hexadecimal number to the new decimal number, which will be the card_id sent to the API
    converted_altered_hex_num = str (int (altered_hex_num,16))
    #print (converted_altered_hex_num)
    
    if len (converted_altered_hex_num) == 9:
        glob_vars.card_id = str ("0" + converted_altered_hex_num)      
    else :   
        glob_vars.card_id = converted_altered_hex_num
    
    #print (config.card_id)
    #print (len (config.card_id))