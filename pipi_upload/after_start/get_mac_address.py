import sys
sys.path.append('/home/bluebox/pipi_reader/pipi_upload')

from network_check import get_mac_address
from time import sleep
from lcd_display import display


mac_address = get_mac_address ()
display ("Checking MAC address","","","")
mac_address_file = "/home/bluebox/mac_address.txt"
f = open (mac_address_file, "w")
f.write (mac_address)
f.close() 
display ("MAC address:",mac_address,"","")
sleep (1)



