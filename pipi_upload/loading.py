import LCD_display
from time import sleep
import config


LCD_display.display ("Loading packages.","Please wait.", "" ,"" ,clear=True, backlight_status=True, sleep=5)

from network_check import network_check

#Check internet connection, acquire IP address and MAC address
try:
    network_check ()
except Exception as network_error:
    LCD_display.display ("Network Error",str(network_error),"" ,"" ,True, True, 2) 

if config.online_status == True :

    from github_check import github_check

    #Connect to GIT HUB and download the latest version from "main", "develop", "pipired" branch   
    try:
        github_check (branch = "develop")    
    except Exception as github_error:
        LCD_display.display ("Repository error", github_error,"" ,"",clear=True, backlight_status=True,sleep=2) 

    try:
        LCD_display.display ("Loading program","","" ,"",clear=True, backlight_status=True, sleep=3)
        import pipi_reader_main
    except Exception as pipi_reader_main_Error:
        LCD_display.display ("Main program error",pipi_reader_main_Error,"" ,"",clear=True, backlight_status=True)    
        print (pipi_reader_main_Error)
        
else:
    LCD_display.display ("No internet"," connection.","Please check cable" ,"Please check wifi" ,True, True, 2) 
