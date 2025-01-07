from datetime import datetime, timedelta
import asyncio


class ButtonCounter:
    def __init__(self):
        self.counter = 0
        self.reset_timer_task = None
        # self.double_press_window = 2

    async def reset_counter(self):
        """Wait for 2 seconds, then reset the counter."""
        await asyncio.sleep(1)
        print("Timer expired. Resetting counter.")
        self.counter = 0

    async def button_pressed(self):
        """Handle button press and manage the reset timer."""
        self.counter += 1
        # print(f"Button pressed. Counter = {self.counter}")

        # Cancel the previous timer if it exists
        if self.reset_timer_task and not self.reset_timer_task.done():
            self.reset_timer_task.cancel()

        # Start a new timer to reset the counter after 2 seconds
        self.reset_timer_task = asyncio.create_task(self.reset_counter())

        # Perform actions based on counter
        if self.counter == 1:
            # pass
            print("Action for counter 1")
        elif self.counter == 2:
            # pass
            print("Action for counter 2")
        elif self.counter == 3:
            # print("Action for counter 3: Resetting counter")
            self.counter = 0  # Reset counter immediately

        return self.counter

        """
        current_time = datetime.now()

        if self.start_time is None or current_time - self.start_time > timedelta(
            seconds=self.double_press_window
        ):
            # Reset the counter and start time if more than 2 seconds have passed since the first press
            # print("Counter reset")
            self.counter = 0
            self.start_time = current_time

            self.counter += 1

            print(f"Button pressed, counter = {self.counter}")

            if self.counter == 1:
                print("Action for counter 1")
                await asyncio.sleep(self.double_press_window)

                if self.counter == 1:
                    print("Final action for counter 1")
                    self.counter = 0

            elif self.counter == 2:
                print("Action for counter 2")

            elif self.counter == 3:
                print("Action for counter 3, reset counter")
                self.counter = 0
"""
