
from log import open_sh, write_log
print ("marker1")


from datetime import datetime
print ("marker2")
from lcd_display import display
print ("marker3")

import glob_vars
print ("marker4")

from network_check import connection_check
print ("marker5")
from pipi_reader_main import main
print ("marker6")






#Check internet connection, acquire IP address and MAC address
try:
    connection_check ()  
    glob_vars.online_status = True
    
except Exception as network_error:
    display ("Network Error",str(network_error),"" ,"" ,True, True, 2) 


display ("Loading packages.","Please wait.", "" ,"" ,clear=True, backlight_status=True, sleep=2)
if glob_vars.online_status == True :
    
    display ("Loading program","","" ,"",True,True, 2)
    
    
    open_sh(glob_vars.mac_address)   
    write_log(1, datetime.now())
    write_log(2, glob_vars.ip_eth0, datetime.now())
    write_log(3, glob_vars.ip_wlan0, datetime.now())
    
    main ()

else:
    display ("No internet"," connection.","Please check cable" ,"Please check wifi" ,True, True, 2) 
