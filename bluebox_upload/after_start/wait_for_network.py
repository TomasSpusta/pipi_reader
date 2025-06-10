import sys
sys.path.append('pipi_upload')

from lcd_display import display

#This will be displayed on RPi after turn on, while it is searching for the network connection (either LAN or Wifi)
display("Waiting for network","","","", clear=True, backlight_status=True)