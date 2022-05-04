#@reboot python3 /home/pi/RFID/client_pokus_RFID.py
#sudo killall python3


import time
import RPi.GPIO as GPIO
import LCD_things
import reader_requests_things

logged_in = False


def main_script():
           
    rfid_number = reader_requests_things.RFID_reader()
    #print ('RFID number from reader: ' + str(rfid_number))
    
    server_response = reader_requests_things.send_receive_data(rfid_number)
    
    #print (server_response)
    
    if logged_in == False:
        LCD_things.LCD_waiting()
    else:
       LCD_things.LCD_logged_in (server_response)
    
    time.sleep(1)
    
    
   

try:
    LCD_things.LCD_waiting()
    while 1:
        main_script()

finally:
    time.sleep(0.5)
    
    GPIO.cleanup()
