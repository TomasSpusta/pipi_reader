

import requests
import time
import config
import sys
import unidecode
from datetime import datetime
import LCD_display
from log import write_log






#sys.path.append('/home/bluebox')
#import equipment_id
#token_address = "pipi_upload/tokenData.txt"
#token_address = "/home/bluebox/pipi_reader/pipi_upload/tokenData.txt"


#token_address = "tokenData.txt"





def crm_request_mac ():
    #mac_address = str (mac_address)
    payload = {"mac_address":config.mac_address}
    try:
        crm_response = requests.post ("https://crm.api.ceitec.cz/get-equipment-by-mac-address", json = payload)
        crm_data = crm_response.json()
        #print (crm_data)
        
        if len (crm_data) == 0:
            print ("Problem with mac address")
            write_log(5, crm_data,datetime.now())
            #if len(data) == 0 that means that something is wrong with mac address or equipment
            
        else:          
            config.equipment_name = crm_data[0]["alias"]
            config.equipment_id = crm_data[0]["equipmentid"]
            write_log(5,config.equipment_name,datetime.now())
            
            #print ("Equipment ID is {} a Equipment Name is {}" .format(config.equipment_id, config.equipment_name))
            
    except Exception as crm_mac_e:
        
        print("Error in crm_request_mac: " + str(crm_mac_e))
        write_log(5,crm_mac_e,datetime.now())
        LCD_display.display("crm_request_mac E", str(crm_mac_e),"","",True,True,2)
    
        
def crm_request_rfid ():
    #scanned_rfid = str (scanned_rfid)
    config.log_row += 1 
    write_log(1,datetime.now())
    print ("------------------------CARD SWIPE------------------------")
    
    payload = {"rfid":config.card_id}
    
    try:
        crm_response = requests.post ("https://crm.api.ceitec.cz/get-contact-by-rfid", json = payload)
        crm_data = crm_response.json()
        #print (crm_data)
        
        if len (crm_data) == 0:
            config.in_database = False
            print ("Problem with ID card, not in database")
            write_log(8,datetime.now(), config.card_id)
            #if len(data) == 0 that means that rfid number is not in database
            #print ('Card is not in the database')       
        else:          
            config.in_database = True
            user_name = crm_data[0]["firstname"]
            #config.user_full_name = crm_data[0]["full_name"]
            config.user_name = unidecode.unidecode (user_name)
            config.user_id = crm_data[0]["contactid"]
            write_log(8,config.user_name +" "+  config.user_id,datetime.now())
            #print (config.user_name)
            print ("User ID is {} and User's first name is {}" .format(config.user_id, config.user_name))
             
    except Exception as CRM_request_e:
        write_log(8, CRM_request_e, datetime.now())
        print("Error in crm_request_rfid:")
        print (CRM_request_e)
        LCD_display.display("crm_request_rfid E", str(CRM_request_e),"","",True,True,2)
   
    
def booking_request_start_measurement ():
#API request from Booking system - inputs are user_ID, instrument_ID, outputs are remaining_time, number_of_files
    
    payload = {"contactId":config.user_id, "equipmentId":config.equipment_id}
    #payload = {"contact":config.user_id, "equipment":config.equipment_id}
    
    checkToken()
    print ("check token in request start")
    
    headers = {"Authorization" : "Bearer " + config.token}
    
    try:
        #booking_response = requests.get ("https://booking.ceitec.cz/api-public/recording/start-by-contact-equipment",  params = payload)
        booking_response = requests.post ("https://booking.ceitec.cz/api/recording/start/",  json= payload, headers = headers)
        
        
        #print (payload)
        #print ("Booking response:")
        #print(booking_response.url)
        print ("Booking status code: " + str(booking_response.status_code))
        print(booking_response.text)
        #LCD_display.display("Rec Resp", str(booking_response.text),str(booking_response.status_code),"",True,True,2)
        
        
        if booking_response.status_code == 200:
            config.logged_in = True
            config.in_session = True
            #print ("200 - Recording started") 
            booking_data = booking_response.json()
            config.remaining_time = int(booking_data["timetoend"])
            config.recording_id = booking_data["recording"]
            config.reservation_id = booking_data ["reservation"]
            config.reservation_start_time = booking_data["start"]
            #print ("Reservation_ID: " +str (config.reservation_id))
            
            write_log(10, datetime.now(), booking_response.text)
            
            #print ("Remaining time of reservation is {} minutes and recording id is {}" .format(config.remaining_time, config.recording_id))
            
        elif booking_response.status_code == 400:
            config.logged_in = False
            write_log(10, datetime.now(), booking_response.text)
            #print ("400 - Invalid input parameters")     
        
        elif booking_response.status_code == 404:
            config.logged_in = False
            write_log(10, datetime.now(), booking_response.text)
            #print ("404 - Reservation not found for given parameters, or missing reservation session")    
        
        elif booking_response.status_code == 409:
            config.logged_in = True
            config.in_session = True
            #print ("409 - Recording is running")
            booking_data = booking_response.json()
            config.remaining_time = int (booking_data["timetoend"])
            config.recording_id = booking_data["recording"]
            config.reservation_id = booking_data ["reservation"]
            config.reservation_start_time = booking_data["start"]
            #print ("Reservation_ID: " +str (config.reservation_id))
            #print ("Remaining time of reservation is {} minutes and recording id is {}" .format(config.remaining_time, config.recording_id))
            write_log(10, datetime.now(), booking_response.text)        
        elif booking_response.status_code == 500:
            config.logged_in = False
            write_log(10, datetime.now(), booking_response.text)
            #print ("500 - Internal error")  
        
        return booking_response.status_code    
        
    except Exception as start_rec_e:
        LCD_display.display("Start rec E", str(start_rec_e),"","",True,True,2)
        print("Error in booking_request_start_measurement: " + str(start_rec_e))
        
    
    
def booking_request_files ():
    #payload = {"recording":recording_id}
    headers = {"Authorization" : "Bearer " + config.token}
    
    try:
        #booking_response = requests.get ("https://booking.ceitec.cz/api-public/recording/" + str(config.recording_id) + "/raw-data-info")
        booking_response = requests.get ("https://booking.ceitec.cz/api/recording/" + str(config.recording_id) + "/file-info", headers = headers)
     
        #print (booking_response.status_code)
        if booking_response.status_code == 200 or 409:
            booking_data = booking_response.json()
            #print (booking_data)
            #print ("Number of data files: " + str(booking_data["count"]))
            config.files = booking_data["count"]            
        else:
            print ("nejaky problemek s datama")
    except Exception as request_files_e:
        LCD_display.display("Request files E", str(request_files_e),"","",True,True,2)
        print("Error in booking_request_files: " + str (request_files_e))
        
def booking_reservation_info ():
    #checkToken()
    headers = {"Authorization" : "Bearer " + config.token}
    #config.logged_in = True
    #config.in_session = True
    try:
        #booking_response = requests.get ("https://booking.ceitec.cz/api-public/service-appointment/" + str(config.reservation_id) + "/")
        booking_response = requests.get ("https://booking.ceitec.cz/api/service-appointment/" + str(config.reservation_id) + "/raspberry", headers=headers)

        
        #print (booking_response.status_code)
        booking_data = booking_response.json()
        #print (booking_data)
        #print ("409 - Recording is running")
        config.remaining_time = int (booking_data["timetoend"])
        #print ("Remaining time of reservation is {} minutes and recording id is {}" .format(config.remaining_time, config.recording_id))
        
    except Exception as res_info_e:
        LCD_display.display("Res info E", res_info_e,"","",True,True,2)
        print("Error in booking_reservation_info: " + str(res_info_e))
        
        

def booking_stop_reservation ():
    payload = {"serviceAppointmentId":config.reservation_id, "equipmentId":config.equipment_id}
    headers = {"Authorization" : "Bearer " + config.token}
    try:
        
        #requests.get ("https://booking.ceitec.cz/api-public/recording/stop-by-reservation-equipment/?reservation={}&equipment={}". format (str(config.reservation_id),str(config.equipment_id)))  
        
        booking_response = requests.post ("https://booking.ceitec.cz/api/recording/stop",json=payload,headers=headers)  
    
        print (booking_response.status_code)
        
        #booking_data = booking_response.json()
        #print (booking_data)
        #print ("409 - Recording is running")
        #config.remaining_time = int (booking_data["timetoend"])
        #print ("Remaining time of reservation is {} minutes and recording id is {}" .format(config.remaining_time, config.recording_id))
        
    except Exception as stop_res_e:
        print("Error in booking_stop_reservation: " + str(stop_res_e))
        
        LCD_display.display("stop_res E", str(stop_res_e),"","",True,True,2)
        write_log(11, datetime.now(), stop_res_e)
         
def loadTokenData ():
    print("Loading token data")
    try:
        
        f = open (config.token_address, "r").readlines()
        expiration = f[0][:-1]
        tokenString = f[1]
        config.token_expiration = expiration
        config.token = tokenString
        print("Token data loaded")
    except Exception as load_token_e:
        LCD_display.display("Load Token E", str(load_token_e),"","",True,True,2)
        print (load_token_e)
        
    
    
def getToken ():
    
    API_key = "ude9c6nezyr71i9vf3jdtye18vwdk81s"
    payload = {"apiKey":API_key}  
       
    try: 
        print("Requesting token")
        token_request = requests.post ("https://booking.ceitec.cz/api/login",json=payload)
        token_expiration = token_request.json()["expiresAt"] 
        token = token_request.json()["accessToken"]
        
        print ("New token created")
        write_log(9, datetime.now(), token_expiration)
        print ("Saving token data")
        
        
        f = open (config.token_address, "w")
        f.writelines([token_expiration + "\n", token])
        f.close()  
      
    except Exception as get_token_e :

        print ("Error in get_token: " + get_token_e)
        LCD_display.display("Get Token E", str(get_token_e),"","",True,True,2)
        write_log(9, datetime.now(), get_token_e)


def checkToken():
    try:
        #print("Comparing dates")
        time_now = datetime.now().isoformat(timespec="seconds")      
        timeNow = datetime.strptime(time_now,"%Y-%m-%dT%H:%M:%S")
        tokenExpiration = datetime.strptime(config.token_expiration,"%Y-%m-%dT%H:%M:%S")
        
        #print ("time now: " + str(timeNow))
        #print ("time exp: " + str(tokenExpiration)) 
        #print(timeNow <= tokenExpiration)
        
        if tokenExpiration <= timeNow:
            print("Token is old, requesting new token")
            #LCD_display.display("Token","is old," ,"requesting","new one",True,True,2)
            getToken()
            print("New token created")
            #LCD_display.display("Token Created"," " ,"","",True,True,2)
            loadTokenData ()
            print("New token loaded")
            #LCD_display.display("Token Loaded"," " ,"","",True,True,2)
        else:
            #LCD_display.display("Token is valid","" ,"","",True,True,2)
            #print("Token is valid")
            pass
    except Exception as check_token_e:
        print (check_token_e)
        LCD_display.display("Check Token E", str(check_token_e),"","",True,True,2)
        write_log(9, datetime.now(), check_token_e)

#loadTokenData()
