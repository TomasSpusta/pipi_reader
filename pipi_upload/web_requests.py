import requests
import config
import unidecode
from datetime import datetime
from lcd_display import display
from log import write_log

def crm_request_name_by_mac ():
   
    try:
        payload = {"mac_address":config.mac_address}
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
        display("crm_request_mac E", str(crm_mac_e),"","",True,True,2)
    
        
def crm_request_user_by_rfid ():
    
    config.log_row += 1 
    print ("------------------------CARD SWIPE------------------------")
    write_log(1,datetime.now())
        
    payload = {"rfid":config.card_id}
    
    try:
        crm_response = requests.post ("https://crm.api.ceitec.cz/get-contact-by-rfid", json = payload)
        crm_data = crm_response.json()
        
        #if len(data) == 0 that means that rfid number is not in database
        if len (crm_data) == 0:
            config.in_crm = False
            print ("Problem with ID card, not in database")
            write_log(8,datetime.now(), config.card_id)
            display ("Your card","is not in database.","Please register it","in booking system.",True, True,5)
            
        else:          
            config.in_crm = True
            user_name = crm_data[0]["firstname"]
            #config.user_full_name = crm_data[0]["full_name"]
            config.user_name = unidecode.unidecode (user_name)
            config.user_id = crm_data[0]["contactid"]
            write_log(8,config.user_name +" "+  config.user_id,datetime.now())
            print ("User ID is {} and User's first name is {}" .format(config.user_id, config.user_name))
            display ("User check.","User in database.","" ,"",True, True, 2)
             
    except Exception as crm_request_e:
        write_log(8, crm_request_e, datetime.now())
        print("Error in crm_request_rfid: " + str(crm_request_e) )
        display("crm_request_rfid E", str(crm_request_e),"","",True,True,2)
   
    
def booking_request_start_recording ():
#API request from Booking system - inputs are user_ID, instrument_ID, outputs are remaining_time, number_of_files
    
    payload = {"contactId":config.user_id, "equipmentId":config.equipment_id}
    #payload = {"contact":config.user_id, "equipment":config.equipment_id}
    
    checkToken()
    print ("check token in request start")
    
    headers = {"Authorization" : "Bearer " + config.token}
    
    try:
        booking_response = requests.post ("https://booking.ceitec.cz/api/recording/start/",  json= payload, headers = headers)
               
        print ("Start recording status code: " + str(booking_response.status_code))
        print(booking_response.text)
               
        if booking_response.status_code == 200:
            config.recording_started = True
            config.in_session = True
           
            booking_data = booking_response.json()
            config.remaining_time = int(booking_data["timetoend"])
            config.recording_id = booking_data["recording"]
            config.reservation_id = booking_data ["reservation"]
            config.reservation_start_time = booking_data["start"]
                        
            write_log(10, datetime.now(), booking_response.text)
            
            #print ("Remaining time of reservation is {} minutes and recording id is {}" .format(config.remaining_time, config.recording_id))
            
        elif booking_response.status_code == 400 or 404 or 500:
            config.recording_started = False
            write_log(10, datetime.now(), booking_response.text)
            #print ("400 - Invalid input parameters")     
                
        '''
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
            write_log(10, datetime.now(), booking_response.text)'''
        
        return booking_response.status_code    
        
    except Exception as start_rec_e:
        display("Start rec E", str(start_rec_e),"","",True,True,2)
        print("Error in booking_request_start_measurement: " + str(start_rec_e))
        
    
    
def booking_request_files ():
    #payload = {"recording":recording_id}
    headers = {"Authorization" : "Bearer " + config.token}
    
    try:
        #booking_response = requests.get ("https://booking.ceitec.cz/api-public/recording/" + str(config.recording_id) + "/raw-data-info")
        booking_response = requests.get ("https://booking.ceitec.cz/api/recording/" + str(config.recording_id) + "/file-info", headers = headers)
     
        #print (booking_response.status_code)
        if booking_response.status_code == 200:
            booking_data = booking_response.json()
            #print (booking_data)
            #print ("Number of data files: " + str(booking_data["count"]))
            config.files = booking_data["count"]            
        else:
            print ("nejaky problemek s datama")
    except Exception as request_files_e:
        display("Request files E", str(request_files_e),"","",True,True,2)
        print("Error in booking_request_files: " + str (request_files_e))
        
def booking_reservation_info ():
    #checkToken()
    headers = {"Authorization" : "Bearer " + config.token}
    
    
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
        display("Res info E", res_info_e,"","",True,True,2)
        print("Error in booking_reservation_info: " + str(res_info_e))
        
        

def booking_stop_recording ():
    payload = {"serviceAppointmentId":config.reservation_id, "equipmentId":config.equipment_id}
    headers = {"Authorization" : "Bearer " + config.token}
    try:      
        booking_response = requests.post ("https://booking.ceitec.cz/api/recording/stop",json=payload,headers=headers)  
        print (booking_response.status_code)
        write_log(11, datetime.now(), "Ended by time")
        
    except Exception as stop_res_e:
        print("Error in booking_stop_reservation: " + str(stop_res_e))
        display("stop_res E", str(stop_res_e),"","",True,True,2)
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
        write_log(10,"Token loaded" ,datetime.now())
    except Exception as load_token_e:
        display("Load Token E", str(load_token_e),"","",True,True,2)
        write_log(10, datetime.now(), load_token_e)
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
        write_log(9, datetime.now(), "Token will expire: \n" + token_expiration)
        print ("Saving token data")
        
        
        f = open (config.token_address, "w")
        f.writelines([token_expiration + "\n", token])
        f.close()  
      
    except Exception as get_token_e :

        print ("Error in get_token: " + get_token_e)
        display("Get Token E", str(get_token_e),"","",True,True,2)
        write_log(9, datetime.now(), get_token_e)


def checkToken():
    try:

        time_now = datetime.now().isoformat(timespec="seconds")      
        timeNow = datetime.strptime(time_now,"%Y-%m-%dT%H:%M:%S")
        tokenExpiration = datetime.strptime(config.token_expiration,"%Y-%m-%dT%H:%M:%S")

        
        if tokenExpiration <= timeNow:
            print("Token is old, requesting new token")
           
            getToken()
            print("New token created")
           
            loadTokenData ()
            print("New token loaded")
           
        else:
           
            #print("Token is valid")
            pass
    except Exception as check_token_e:
        print (check_token_e)
        display("Check Token E", str(check_token_e),"","",True,True,2)
        write_log(9, datetime.now(), check_token_e)


