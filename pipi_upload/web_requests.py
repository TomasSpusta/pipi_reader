
from mfrc522 import SimpleMFRC522
import requests
import time
import config

#create RFID reader instance
reader = SimpleMFRC522() 


def rfid_reader():
    config.card_id, text = reader.read()
    #print ('Readed card: ' + str(rfid))
    

#Function dealing with sending and recieving the data.
#Parameter rfid is card number from MFRC522 reader

def crm_request_mac ():
    #mac_address = str (mac_address)
    payload = {"mac_address":config.mac_address}
    try:
        crm_response = requests.post ("https://betacrm.api.ceitec.cz/get-equipment-by-mac-address", json = payload)
        crm_data = crm_response.json()
        #print (crm_data)
        
        if len (crm_data) == 0:
            print ("Problem with mac address")
            #if len(data) == 0 that means that something is wrong with mac address or equipment
            
        else:          
            config.equipment_name = crm_data[0]["alias"]
            config.equipment_id = crm_data[0]["equipmentid"]
            print ("Equipment ID is {} a Equipment Name is {}" .format(config.equipment_id, config.equipment_name))
            
    except Exception as e:
        print("Error in crm_request_mac")
        print (e)
    
        
def crm_request_rfid ():
    #scanned_rfid = str (scanned_rfid)
    payload = {"rfid":config.card_id}
    
    try:
        crm_response = requests.post ("https://betacrm.api.ceitec.cz/get-contact-by-rfid", json = payload)
        crm_data = crm_response.json()
        #print (crm_data)
        
        if len (crm_data) == 0:
            config.in_database = False
            print ("Problem with ID card, not in database")
            #if len(data) == 0 that means that rfid number is not in database
            #print ('Card is not in the database')       
        else:          
            config.in_database = True
            config.user_name = crm_data[0]["firstname"]
            config.user_id = crm_data[0]["contactid"]
            #print (config.user_name)
            print ("User ID is {} and User's first name is {}" .format(config.user_id, config.user_name))
             
    except Exception as e:
        print("Error in crm_request_rfid:")
        print (e)
   
    
def booking_request_start_measurement ():
#API request from Booking system - inputs are user_ID, instrument_ID, outputs are remaining_time, number_of_files
   
   #### THIS NEEDS TO BE COMMENTED OUT IN REAL SITUATION 
    # RFID-TEST:
    # config.equipment_id = "45856b41-8ae8-ec11-80cd-005056914121"     
    
    # KERR-MICROSCOPE:
    config.equipment_id = "907ebc62-37f1-e711-8b1a-005056991551"
   #### THIS NEEDS TO BE COMMENTED OUT IN REAL SITUATION
    
    
    payload = {"contact":config.user_id, "equipment":config.equipment_id}

    try:
        booking_response = requests.get ("https://booking.ceitec.cz/api-public/recording/start-by-contact-equipment",  params = payload)
        
        #print ("Booking response:")
        #print ("Booking status code:")
        #print(booking_response.status_code)
        
        if booking_response.status_code == 200:
            config.logged_in = True
            config.in_session = True
            #print ("200 - Recording started") 
            booking_data = booking_response.json()
            config.remaining_time = int(booking_data["timetoend"])
            config.recording_id = booking_data["recording"]
            #print ("Remaining time of reservation is {} minutes and recording id is {}" .format(config.remaining_time, config.recording_id))
            
        elif booking_response.status_code == 400:
            config.logged_in = False
            #print ("400 - Invalid input parameters")     
        
        elif booking_response.status_code == 404:
            config.logged_in = False
            #print ("404 - Reservation not found for given parameters, or missing reservation session")    
        
        elif booking_response.status_code == 409:
            config.logged_in = True
            config.in_session = True
            #print ("409 - Recording is running")
            booking_data = booking_response.json()
            config.remaining_time = int (booking_data["timetoend"])
            config.recording_id = booking_data["recording"]
            #print ("Remaining time of reservation is {} minutes and recording id is {}" .format(config.remaining_time, config.recording_id))
        elif booking_response.status_code == 500:
            config.logged_in = False
            #print ("500 - Internal error")  
        
        return booking_response.status_code    
        
    except Exception as e:
        print("Error in booking_request_start_measurement")
        print(e)
    
    
def booking_request_files ():
    #payload = {"recording":recording_id}
    
    try:
        booking_response = requests.get ("https://booking.ceitec.cz/api-public/recording/" + str(config.recording_id) + "/raw-data-info")
        
        #print (booking_response.status_code)
        if booking_response.status_code == 200 or 409:
            booking_data = booking_response.json()
            #print (booking_data)
          # print (booking_data["filesCount"])
            config.files = booking_data["filesCount"]            
        else:
            print ("nejaky problemek s datama")
    except Exception as e:
        print("Error in booking_request_files")
        print(e)
    
