from datetime import datetime
import glob_vars
from getmac import get_mac_address as gma  # module for mac adress
from lcd_display import display
import web_requests

import netifaces as ni
from log import write_log, open_sh
from log_temp import write_log_temp



def connection_check(): 

    get_ip()
    load_mac_address ()
    
    # Send request to CRM to obtain equipment info according to MAC address
    web_requests.crm_request_equipment_by_mac()
    
    if glob_vars.ip_eth0 != 0:
        display ("IP:",glob_vars.ip_eth0,"MAC:",glob_vars.mac_address)
    else:
        display ("IP:",glob_vars.ip_wlan0,"MAC:",glob_vars.mac_address)
    
    print("Equipment name: " + str(glob_vars.equipment_name))
    print("Equipment ID: " + str(glob_vars.equipment_id))

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
        glob_vars.ip_eth0 = ip_lan
    if ip_wifi != 0:
        glob_vars.ip_wlan0 = ip_wifi

def get_mac_address ():
    try:
        mac_address = gma()  # get MAC address
        print("My MAC adress is: {}".format(mac_address))
        write_log_temp ("MAC address: " + mac_address)
        return mac_address

    
    except Exception as mac_e:
        write_log_temp ("Get MAC error: " + str(mac_e))
        print("Get MAC error: " + str(mac_e))

def load_mac_address ():
    mac_address_file = "/home/bluebox/pipi_reader/pipi_upload/mac_address.txt"
    f = open (mac_address_file, "r")
    glob_vars.mac_address = f.read ()
    f.close() 
    