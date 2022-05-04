# This script will run as the first script - initialization, on RPi start-up
#1: Need to check internet connection => 
    #Display IP adress, 
    #if not connected, wait x seconds and check again, after 10 iterations of waiting, show, there is no internet connection
#2: Check and display the Mac adress of the RPi
#3: Run "pipi_reader_main.py"

#from rpi_lcd import LCD
from requests import get
from getmac import get_mac_address as gma

def LCD_disp(ip, mac):
    lcd = LCD() #create LCD dispaly instance
    lcd.clear() #clear the display
    lcd.text("Hi! Welcome" , 1)  #print/show string on line 2
    lcd.text("Please log in", 2) #print/show string on line 3
    lcd.text("with your user card",3)




ip = get('https://api.ipify.org').content.decode('utf8')
mac = gma()
print('My public IP address is: {}'.format(ip))
print("My MAC adress is: {}".format(mac))