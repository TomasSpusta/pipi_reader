import requests
import config
import web_requests

scanned_rfid = 912853855591
mac_address = "e4:5f:01:8d:6d:3f"
user_id =  "2c5c963c-68ba-e311-85a1-005056991551"
equipment = "45856b41-8ae8-ec11-80cd-005056914121"
recording_id = "a90e2dbc-2ef6-ec11-80cd-005056914121"


web_requests.crm_request_mac (mac_address)
web_requests.crm_request_rfid (scanned_rfid)

config.equipment_id = "45856b41-8ae8-ec11-80cd-005056914121"
web_requests.booking_request_start_measurement (config.user_id, config.equipment_id)

#print(config.equipment_id)
#config.recording_id = "1298650f-14f6-ec11-80cd-005056914121"
web_requests.booking_request_files ("a90e2dbc-2ef6-ec11-80cd-005056914121")
print(("https://booking.ceitec.cz/api-public/recording/" + str(recording_id) + "/raw-data-info"))
