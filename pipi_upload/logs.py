import logging
import config

logging.basicConfig (filename="_pipi_log.log", level=logging.INFO, format=	
'%(asctime)s:%(message)s')

def start():
    
    #print ("Remaining time of reservation is {} minutes and recording id is {}" .format(config.remaining_time, config.recording_id))
    logging.info (("\n User ID: {}\n Card ID: {}\n User name: {}\n Equipment ID: {}\n Equipment alias: {}\n Reservation ID: {}\n Recording ID: {}"
                   .format(config.user_id, config.card_id, config.user_name,
                           config.equipment_id, config.equipment_name, 
                           config.reservation_id, config.recording_id)))


    
    
    
    
    
    ''',
        
        config.mac_address, config.card_id
    
    )
    '''
'''
user_id = ""
user_name = ""

equipment_id = ""
equipment_name = ""

reservation_id = ""
recording_id = ""
remaining_time = 0
files = 0
warning_sent = False

in_database = False
logged_in = False
in_session = False

status_code = 0

reservation_start_time = "" 
    
'''    
def end():
    logging.info ( "end",
    
        config.mac_address, config.card_id
    )
    
 