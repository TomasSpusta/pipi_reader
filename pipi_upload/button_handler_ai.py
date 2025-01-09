from gpiozero import Button


class ButtonHandler:
    def __init__(self, pin=21):
        self.button = Button(pin)

    def set_callback(self, callback):
        try:
            self.button.when_pressed = callback
        except Exception as e:
            print(f"Error setting button callback: {e}")
