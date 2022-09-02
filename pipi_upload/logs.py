import logging
import config

logging.basicConfig (filename="_pipi_log.log", level=logging.INFO, format=	
'%(asctime)s:%(message)s')

def start():
    
  
    logging.info ((("\n--LOG on session START-- \
                    \n Instrument info:     \
                    \n MAC Address: {}     \
                    \n Equipment ID: {}     \
                    \n Equipment alias: {}  \
                    \n                      \
                    \n User info:           \
                    \n User ID: {}          \
                    \n Card ID: {}          \
                    \n User name: {}        \
                    \n                      \
                    \n Reservation info:     \
                    \n Reservation ID: {}   \
                    \n Recording ID: {}     \
                    \n") 
                   .format( 
                    config.mac_address, config.equipment_id, config.equipment_name,
                    config.user_id, config.card_id, config.user_full_name,
                    config.reservation_id, config.recording_id
                    )))


    
   
def end():
    logging.info ((("\n--LOG on session END-- \
                    \n Instrument info:     \
                    \n MAC Address: {}     \
                    \n Equipment ID: {}     \
                    \n Equipment alias: {}  \
                    \n                      \
                    \n User info:           \
                    \n User ID: {}          \
                    \n Card ID: {}          \
                    \n User name: {}        \
                    \n                      \
                    \n Reservation info:     \
                    \n Reservation ID: {}   \
                    \n Recording ID: {}     \
                    \n"
                    ) 
                   .format( 
                    config.mac_address, config.equipment_id, config.equipment_name,
                    config.user_id, config.card_id, config.user_full_name,
                    config.reservation_id, config.recording_id
                    )))
    
 