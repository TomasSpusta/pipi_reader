from LCD_display import display
import netifaces as ni



try:
    ip_eth0 = ni.ifaddresses ("eth0")[ni.AF_INET][0]["addr"]         
except Exception as ip_e_eth0:
    print (ip_e_eth0)

try:
    ip_wlan0 = ni.ifaddresses ("wlan0")[ni.AF_INET][0]["addr"]       
except Exception as ip_e_wlan0:
    print (ip_e_wlan0)


try:
    display(ip_eth0,ip_e_eth0,ip_wlan0,ip_e_wlan0, True, True, 2
    )
except Exception as e:
    display(        str(e),        " ",        " ",        " ", True, True, 2
    )