
from log import open_sh, write_log
from datetime import datetime
from lcd_display import display
import glob_vars
from network_check import connection_check
from pipi_reader_main import main

#Check internet connection, acquire IP address and MAC address
try:
    connection_check ()  
    glob_vars.online_status = True
    
except Exception as network_error:
    display ("Network Error",str(network_error),"" ,"" ,True, True, 2) 


display ("Loading packages.","Please wait.", "" ,"" ,clear=True, backlight_status=True, sleep=2)
if glob_vars.online_status == True :
    
    display ("Loading program","","" ,"",True,True, 2)
    
    
    open_sh()   
    write_log(1, datetime.now())
    write_log(2, glob_vars.ip_eth0, datetime.now())
    write_log(3, glob_vars.ip_wlan0, datetime.now())
    write_log(5, glob_vars.equipment_name, datetime.now())
    write_log(14, "Branch: main")
    
    main ()

   

else:
    display ("No internet"," connection.","Please check cable" ,"Please check wifi" ,True, True, 2) 
