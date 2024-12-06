from gpiozero import Button
from lcd_display import display, backlight
import time
import asyncio


class ButtonHandler:
    def __init__(self, pin: int, backlight_callback, display_callback) -> None:
        self.button = Button(pin)
        backlight_callback = backlight_callback
        display_callback = display_callback

    def activate_btn(self):
        print("Button activated")
        GPIO.add_event_detect(self.pin, GPIO.BOTH,
                              callback=self.btn_callback, bouncetime=50)

    def deactivate_btn(self):
        GPIO.remove_event_detect(self.pin)  # Remove event listener
        GPIO.cleanup(self.pin)

    def btn_callback(self, pin: int) -> None:

        if GPIO.input(pin) == GPIO.HIGH:
            print("Button released")
            backlight(False)
            return False

        else:
            print("Button Pressed")
            self.handle_btn_hold()

    def handle_btn_hold(self) -> None:
        hold_time = 1.5
        increments = 18
        counter = 0

        while GPIO.input(self.pin) == GPIO.LOW:
            backlight(True)
            counter += 1

            time.sleep(hold_time/increments)

            if counter > increments:
                display('Session ended', 'by user', "", "",
                        clear=True, backlight_status=True)
                return True

                # booking_stop_recording()
                #write_log(11, datetime.now(), "Ended by user")
                #glob_vars.ended_by_user = True
                # time.sleep(2)
