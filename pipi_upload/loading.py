import LCD_display
from time import sleep


LCD_display.display ("Loading packages.","Please wait.", "" ,"" ,clear=True, backlight_status=True)
sleep (5)

from network_check import network_check

#Check internet connection, acquire IP address and MAC address
try:
    network_check ()
except Exception as network_error:

    LCD_display.display (network_error,"","" ,"",clear=True, backlight_status=True) 

sleep (1)

from github_check import github_check

#Connect to GIT HUB and download the latest version from "main" or "develop" branch   
try:
    github_check (branch = "develop")    
except Exception as github_error:
    LCD_display.display (github_error,"","" ,"",clear=True, backlight_status=True) 

LCD_display.display ("Loading program","","" ,"",clear=True, backlight_status=True)
sleep (3)
import pipi_reader_main
    
