
from mfrc522 import SimpleMFRC522
import requests
import time
import config

#create RFID reader instance
reader = SimpleMFRC522() 


def RFID_reader():
    scanned_rfid, text = reader.read()
    #print ('Readed card: ' + str(rfid))
    return scanned_rfid 

#Function dealing with sending and recieving the data.
#Parameter rfid is card number from MFRC522 reader

def send_receive_data(scanned_rfid):
    #print (scanned_rfid)
    rfid = str(scanned_rfid)   
    
    #data to be sent to the booking system web api in json format
    payload = {"rfid":rfid}
    
    # try to send the payload to web api, when error it will show on LCD
    try:
        response = requests.post ("https://betacrm.api.ceitec.cz/GetContactByFRID", json = payload)
        #print ('Response from post request: ' + str(response))
        data = response.json()
        #print (data[0]["full_name"]) #Here can be changed what data is pulled out of the API
        #print ('Data from post request: ' + str(data))
        
        #print (len(data))
        if len (data) == 0:
            config.logged_in = True
            #if len(data) == 0 that means that rfid number is not in database
            in_database = False
            #print ('Card is not in the database')
            return in_database
        else:          
            user_full_name = data [0]["full_name"]
            config.logged_in = not config.logged_in
            #print ('User name: ' + str(user_full_name))
            return user_full_name
        
    except:
        server_error = "Server Error"  
        return server_error
    

def get_instrument_name (MAC_address): ### !!! Nutné upraviť až bude hotová API !!!
    payload = {"MAC Address":MAC_address}
    response = requests.post ("https://betacrm.api.ceitec.cz/GetContactByFRID", json = payload)
    data = response.json()
    try:
        instrument_name = data [0]["instrument_name"] 
        print (instrument_name)
        return instrument_name
    
    except Exception as e:
        print (e)
        
def has_reservation (CardID, MAC_address): ### !!! Nutné upraviť až bude hotová API !!!
    payload = {"CardID": CardID, "MAC Address":MAC_address}
    response = requests.post ("https://betacrm.api.ceitec.cz/GetContactByFRID", json = payload)
    data = response.json()
    try:
        has_reservation = data [0]["has_reservation"] 
        print (has_reservation)
        return has_reservation
    
    except Exception as e:
        print (e)
        
def logged_in (CardID, MAC_address, has_reservation): ### !!! Nutné upraviť až bude hotová API !!!
    payload = {"CardID": CardID, "MAC Address":MAC_address, "has_reservation": has_reservation}
    response = requests.post ("https://betacrm.api.ceitec.cz/GetContactByFRID", json = payload)
    data = response.json()
    try:
        logged_in = data [0]["logged_in"] 
        print (logged_in)
        return logged_in
    
    except Exception as e:
        print (e)

def remaining_time (CardID, MAC_address): ### !!! Nutné upraviť až bude hotová API !!!
    payload = {"CardID": CardID, "MAC Address":MAC_address}
    response = requests.post ("https://betacrm.api.ceitec.cz/GetContactByFRID", json = payload)
    data = response.json()
    try:
        remaining_time = data [0]["remaining_time"] 
        print (remaining_time)
        return remaining_time
    
    except Exception as e:
        print (e)