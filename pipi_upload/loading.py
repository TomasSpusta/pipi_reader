from datetime import datetime
import lcd_display
from time import sleep
import config
import web_requests



lcd_display.display ("Loading packages.","Please wait.", "" ,"" ,clear=True, backlight_status=True, sleep=5)

from connection_check import connection_check

#Check internet connection, acquire IP address and MAC address
try:
    connection_check ()  
    
except Exception as network_error:
    lcd_display.display ("Network Error",str(network_error),"" ,"" ,True, True, 2) 

if config.online_status == True :

    from github_check import github_check

    #Connect to GIT HUB and download the latest version from "main", "develop", "pipired" branch   
    try:
        github_check (branch = "develop_logs")    
    except Exception as github_error:
        print (github_error)
        lcd_display.display ("Repository error", github_error,"" ,"",clear=True, backlight_status=True,sleep=2) 
    sleep(3)

    try:
        lcd_display.display ("Loading program","","" ,"",clear=True, backlight_status=True, sleep=3)
        web_requests.loadTokenData()
        import pipi_reader_main
    except Exception as pipi_reader_main_Error:
        lcd_display.display ("Main program error",pipi_reader_main_Error,"" ,"",clear=True, backlight_status=True)    
        print (pipi_reader_main_Error)
        
else:
    lcd_display.display ("No internet"," connection.","Please check cable" ,"Please check wifi" ,True, True, 2) 
