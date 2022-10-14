import requests
#import config
#import web_requests

#config.card_id = 912853855591
#config.mac_address = "b8:27:eb:40:c4:8d"
#config.user_id =  "2c5c963c-68ba-e311-85a1-005056991551"
#config.equipment_id = "45856b41-8ae8-ec11-80cd-005056914121" # equip id of RFID-TEST in real booking system
                       
#config.recording_id = "06ba7430-c81f-ed11-80cf-005056914121"
#config.reservation_id = "f8e69b02-cd1f-ed11-80cf-005056914121"


#web_requests.crm_request_mac ()
#web_requests.crm_request_rfid ()

#config.equipment_id = "45856b41-8ae8-ec11-80cd-005056914121"

#web_requests.booking_request_start_measurement ()
#print (config.reservation_id)
#print(config.equipment_id)
#config.recording_id = "1298650f-14f6-ec11-80cd-005056914121"
#web_requests.booking_request_files ("a90e2dbc-2ef6-ec11-80cd-005056914121")
#print(("https://booking.ceitec.cz/api-public/recording/" + str(recording_id) + "/raw-data-info"))

#config.reservation_id = "5877750e-d01f-ed11-80cf-005056914121"
#config.reservation_id = "5877750e-d01f-ed11-80cf-005056914121"
#web_requests.booking_reservation_info ()
response = requests.get("https://api.github.com/repos/TomasSpusta/pipi_reader/releases/latest")
print(type(response.json()["name"]))
