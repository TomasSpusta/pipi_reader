from datetime import datetime
import globals
from getmac import get_mac_address as gma  # module for mac adress
from lcd_display import display
import web_requests

import netifaces as ni
from log import write_log, open_sh
from log_temp import write_log_temp
import os


def connection_check(): 
    
    get_mac_address()
    
    open_sh(globals.mac_address)   
    
    get_ip()
    
    write_log(1, datetime.now())
    write_log(2, globals.ip_eth0, datetime.now())
    write_log(3, globals.ip_wlan0, datetime.now())

    # Send request to CRM to obtain equipment info according to MAC address
    web_requests.crm_request_name_by_mac()
    
    if globals.ip_eth0 != 0:
        display ("IP:",globals.ip_eth0,"MAC:",globals.mac_address)
    else:
        display ("IP:",globals.ip_wlan0,"MAC:",globals.mac_address)
    
    print("Equipment name: " + str(globals.equipment_name))
    print("Equipment ID: " + str(globals.equipment_id))

def check_lan():
    try:
        ip_eth0 = ni.ifaddresses("eth0")[ni.AF_INET][0]["addr"]
    except Exception as ip_e_eth0:
        print(ip_e_eth0)
        ip_eth0 = 0

    return ip_eth0


def check_wifi():
    try:
        ip_wlan0 = ni.ifaddresses("wlan0")[ni.AF_INET][0]["addr"]
    except Exception as ip_e_wlan0:
        print(ip_e_wlan0)
        ip_wlan0 = 0
    
    return ip_wlan0
    
def get_ip():
    ip_lan = check_lan ()
    ip_wifi = check_wifi ()
    if ip_lan != 0:
        globals.ip_eth0 = ip_lan
    if ip_wifi != 0:
        globals.ip_wlan0 = ip_wifi

def get_mac_address ():
    try:
        globals.mac_address = gma()  # get MAC address
        print("My MAC adress is: {}".format(globals.mac_address))
        write_log_temp ("MAC address: " + globals.mac_address)
    
    except Exception as mac_e:
        write_log_temp ("Get MAC error: " + str(mac_e))
        print(mac_e)
        print("Problem with MAC address")