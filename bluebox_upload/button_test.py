from gpiozero import Button
from signal import pause

button_stop = Button(21)
button_extend = Button (13)

def on_press():
    print ("Button pressed")

def on_release():
    print ("Button released")
    
button_extend.when_pressed = on_press
button_stop.when_pressed = on_press

pause ()
