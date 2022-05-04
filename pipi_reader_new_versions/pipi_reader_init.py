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
    lcd.text("IP adress:" , 1)  #print/show string on line 2
    if ip == 0:
        lcd.text("Not Connected", 2)     
    else:
        lcd.text(ip, 2) #print/show string on line 3
    lcd.text("MAC adress",3)
    lcd.text(mac,4)



try:
    ip = get('https://api.ipify.org').content.decode('utf8')    
except Exception as e:
    ip = 0
    print (e) 
    
mac = gma()
print('My public IP address is: {}'.format(ip))
print("My MAC adress is: {}".format(mac))

LCD_disp (ip, mac)