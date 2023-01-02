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
    # trim the last 2 characters from the hexadecimal number
    trimmed_hex_num = hex_num [2:10:]
    
    #print (trimmed_hex_num)
    
    # translate the entities in hex format to the hex format from PC RFID reader
    altered_hex_num = trimmed_hex_num [6] + trimmed_hex_num [7] + trimmed_hex_num [4] + trimmed_hex_num [5] + trimmed_hex_num [2] + trimmed_hex_num [3] + trimmed_hex_num [0] + trimmed_hex_num [1]
    
    #print (altered_hex_num)
    
    # convert altered hexadecimal number to the new decimal number, which will be the card_id sent to the API
    converted_altered_hex_num = int (altered_hex_num,16)
    
    if len (converted_altered_hex_num) == 9:
        config.card_id = str ("0" + converted_altered_hex_num)      
    else :   
        config.card_id = converted_altered_hex_num
    #print (config.card_id)
    
    # TO DO: there is prbolem with cards starting with 0 ZERO, there needs to be condition, when lenght card_id is 9, add zero on the firrts place.