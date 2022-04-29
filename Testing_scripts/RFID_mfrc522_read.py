import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
#/usr/local/lib/python3.7/dist-packages/mfrc522/MFRC522.py
from time import sleep

reader = SimpleMFRC522()


try:
    while True:
        id, text = reader.read()
        print(id)
        
        sleep(1)
except:
    print ("some error")

finally:
    GPIO.cleanup()

