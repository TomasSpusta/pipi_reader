from mfrc522 import SimpleMFRC522
import requests
import time

reader = SimpleMFRC522() #create RFID reader instance

def RFID_reader():
    rfid, text = reader.read()
    #print ('Readed card: ' + str(rfid))
    return rfid 

#Function dealing with sending and recieving the data.
#Parameter rfid is card number from MFRC522 reader

def send_receive_data(scanned_rfid):
    global logged_in
    #print (scanned_rfid)
    rfid = str(scanned_rfid)       
    payload = {"rfid":rfid}
    try:
        response = requests.post ("https://betacrm.api.ceitec.cz/GetContactByFRID", json = payload)
        #print ('Response from post request: ' + str(response))
        data = response.json()
        #print (data[0]["full_name"]) #Here can be changed what data is pulled out of the API
        #print ('Data from post request: ' + str(data))
        
        #print (len(data))
        if len (data) == 0:
            logged_in = True
            #if len(data) == 0 that means that rfid number is not in database
            in_database = False
            #print ('Card is not in the database')
            return in_database
        else:          
            user_full_name = data [0]["full_name"]
            logged_in = not logged_in
            #print ('User name: ' + str(user_full_name))
            return user_full_name
        
    except:
        server_error = "Server Error"  
        return server_error