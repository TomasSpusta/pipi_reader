import sys
sys.path.append('pipi_upload')

from network_check import get_mac_address
from time import sleep

mac_address = get_mac_address ()

mac_address_file = "/home/bluebox/mac_address.txt"

f = open (mac_address_file, "w")
f.write (mac_address)
f.close() 
sleep (1)


