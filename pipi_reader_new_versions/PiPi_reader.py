#@reboot python3 /home/pi/RFID/client_pokus_RFID.py
#sudo killall python3

import requests
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from rpi_lcd import LCD



logged_in = False
reader = SimpleMFRC522() #create RFID reader instance
lcd = LCD() #create LCD dispaly instance
lcd.backlight (False) #Turn off LCD backlight


def RFID_reader():
    rfid, text = reader.read()
    #print ('Readed card: ' + str(rfid))
    return rfid 


#Function dealing with sending and recieving the data.
#Parameter rfid is card number from MFRC522 reader
def send_receive_data(scanned_rfid):
    global logged_in
    #print (scanned_rfid)
    rfid = str(scanned_rfid)       
    payload = {"rfid":rfid}
    try:
        response = requests.post ("https://betacrm.api.ceitec.cz/GetContactByFRID", json = payload)
        #print ('Response from post request: ' + str(response))
        data = response.json()
        #print (data[0]["full_name"]) #Here can be changed what data is pulled out of the API
        #print ('Data from post request: ' + str(data))
        
        #print (len(data))
        if len (data) == 0:
            logged_in = True
            #if len(data) == 0 that means that rfid number is not in database
            in_database = False
            #print ('Card is not in the database')
            return in_database
        else:          
            user_full_name = data [0]["full_name"]
            logged_in = not logged_in
            #print ('User name: ' + str(user_full_name))
            return user_full_name
        
    except:
        server_error = "Server Error"  
        return server_error

def LCD_waiting ():
    global logged_in
    logged_in = False
    lcd.clear() #clear the display
    lcd.text("Hi! Welcome" , 1)  #print/show string on line 2
    lcd.text("Please log in", 2) #print/show string on line 3
    lcd.text("with your user card",3)
    
def LCD_logged_in (server_response): # function dealing with displaying to the LCD display
    global logged_in
    logged_in = True
    #print ("LCD_section")
    
    if server_response == False:
        #print ("Card is not in database")
        lcd.clear() #clear the display
        lcd.text("Card is not in a database" , 1)  #print/show string on line 1
        lcd.text("Please contact User office" , 3)
        logged_in = False
        time.sleep(5)
        #print (logged_in)
        LCD_waiting()
        
    elif server_response == "Server Error":
        #print ("Server error")
        lcd.clear() #clear the display
        lcd.text("Server Error" , 1)
        logged_in = False
        time.sleep(5)
        LCD_waiting()
        
        
    else:
        lcd.clear() #clear the display
        lcd.text("You are logged as:" , 1)  #print/show string on line 1
        lcd.text(str(server_response), 2) 
        lcd.text ("Happy hunting", 3)
        #lcd.text("Your session ends at:" , 3)  
        #lcd.text ("-end time-", 4)
    
 


def main_script():
           
    rfid_number = RFID_reader()
    #print ('RFID number from reader: ' + str(rfid_number))
    
    server_response = send_receive_data(rfid_number)
    
    #print (server_response)
    
    if logged_in == False:
        LCD_waiting()
    else:
        LCD_logged_in (server_response)
    
    time.sleep(1)
    
    
   
   
if __name__ == "__main__":
    try:
        LCD_waiting()
        while 1:
            main_script()
 
    finally:
        time.sleep(0.5)
        lcd.clear()
        GPIO.cleanup()
