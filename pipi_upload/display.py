from LCD_display import display, clear
import netifaces as ni
from time import sleep



try:
    ip_eth0 = ni.ifaddresses ("eth0")[ni.AF_INET][0]["addr"]         
    print (ip_eth0)
    display(ip_eth0, "","" ,"",  False, True, 2 )
except Exception as ip_e_eth0:
    print (ip_e_eth0)
    display("", ip_e_eth0,"" ,"",  False, True, 2)

try:
    ip_wlan0 = ni.ifaddresses ("wlan0")[ni.AF_INET][0]["addr"]      
    print (ip_wlan0)
    display("" , "",ip_wlan0,"",  False, True, 2 ) 
except Exception as ip_e_wlan0:
    print (ip_e_wlan0)
    display("" , "","",ip_e_wlan0,  False, True, 2 ) 

'''
try:
    display(ip_eth0,ip_e_eth0,ip_wlan0,ip_e_wlan0, True, True, 2
    )
except Exception as e:
    display(        str(e),        " ",        " ",        " ", True, True, 2
    )
'''

sleep (10)
clear()