from lcd_display import LCDController
import inspect
import random
import sys


class Screens:
    def __init__(self, lcd_controller: LCDController):
        self.lcd = lcd_controller

    async def starting_screen(self):
        await self.lcd.message(
            "Starting...",
            display_time=0.1,
        )

    async def welcome_screen(self, instrument_name: str):
        await self.lcd.message(
            "Welcome at",
            f"{instrument_name}",
            "Please log in",
            "with your card",
            display_time=0.1,
        )

    # User
    async def checking_user(self):
        await self.lcd.message(
            "Checking user...",
            # display_time=0.5,
        )

    async def user_ok(self, user_name: str):
        phrases = [
            "Push the boundaries!",
            "Unleash your genius!",
            "Answers lie ahead!",
            "Discovery awaits!",
            "Keep exploring!",
            "Truth is out there!",
            "Find the unknown!",
        ]

        async def random_phase() -> str:
            phrase = random.choice(phrases)
            return phrase

        await self.lcd.message(
            f"Hi {user_name}",
            f"{await random_phase()}",
            # display_time=0.5,
        )

    async def user_not_in_database(self):
        await self.lcd.message(
            "Card not registered.",
            "Please register it.",
            # display_time=0.1,
        )

    # Reservation
    async def checking_reservation(self):
        await self.lcd.message(
            "Checking reservation",
            # display_time=0.1,
        )

    async def reservation_ok(self):
        await self.lcd.message(
            "Reservation found.",
            "Starting session...",
            "",
            "",
            # display_time=0.1,
        )

    async def reservation_nok(self):
        await self.lcd.message(
            "No reservation",
            "in next 30 minutes.",
            "Please make one.",
            # display_time=0.1,
        )

    # Session

    async def in_session(self, remaining_session_time: int):
        await self.lcd.message(
            "Remaining time:",
            f"{remaining_session_time} minutes",
            "",
            "Button->BUTTON_MENU",
            display_time=5,
            backlight=False,
        )

    async def session_ended_by_timeout(self):
        await self.lcd.message(
            "Your session ended.",
            "See you next time.",
            # display_time=0.1,
        )

    async def session_ended_by_user(self):
        await self.lcd.message(
            "User ended session.",
            "See you nex time.",
            # display_time=0.1,
        )

    async def session_end_warning(self, remaining_session_time: int):
        await self.lcd.flashing(0.3, 5)
        await self.lcd.message(
            "Session will end in",
            f"{remaining_session_time} minutes.",
            "To extend session",
            "use BUTTON MENU.",
            # display_time=5,
        )
        
    async def session_extended (self):
        await self.lcd.message(
            "Your session",
            "was extended",
            "by 15 minutes",
        )    

    # Error
    async def error_message(self, error: str, source_function="Unknown"):
        await self.lcd.message(
            f"F:{source_function[:18]}",
            error[:20],
            error[20:],
            display_time=5,
        )
        # sys.exit("Critical Error. Stopping the program.")

    # Button menu
    async def button_menu(
        self,
        selected_row,
    ):
        # Format the display with '>' at the selected row
        options = ["Back", "Extend session", "Supervisor mode", "End session"]
        display_lines = []
        for i, option in enumerate(options):
            if i == selected_row:
                display_lines.append(f"> {option}")
            else:
                display_lines.append(f"  {option}")

        await self.lcd.message(
            display_lines[0],
            display_lines[1],
            display_lines[2],
            display_lines[3],
            display_time=0.1,
        )

    async def button_menu_extend(self):
        await self.lcd.message(
            "Scan your card",
            "to extend session",
            "by 15 minutes.",
            "Waiting...",
            display_time=0.1,
        )

    async def button_menu_extend_ok(self):
        await self.lcd.message(
            "Session extended",
            "by 15 minutes.",
            # display_time=0.1,
        )

    async def button_menu_extend_not_yet(self):
        await self.lcd.message(
            "Session can be",
            "extended only",
            "15 minutes",
            "before its end.",
            # display_time=0.1,
        )

    async def button_menu_extend_bad_card(self):
        await self.lcd.message(
            "Unauthorized user",
            "Session not extended",
            "Returning to session",
            # display_time=0.1,
        )

    async def button_menu_end_confirmation(self):
        await self.lcd.message(
            "Press button",
            "to confirm",
            "session end.",
            # display_time=0.1,
        )

    async def run_all_screens(self):
        """Programmatically run all screen display methods for testing."""
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and attr_name not in ["run_all_screens", "__init__"]:
                if inspect.iscoroutinefunction(attr):
                    params = inspect.signature(attr).parameters
                    args = []

                    # Generate default arguments for each parameter
                    for param in params.values():
                        if param.default != inspect.Parameter.empty:
                            args.append(
                                param.default
                            )  # Use the default value if it exists
                        elif param.annotation is int:
                            args.append(0)  # Default int
                        elif param.annotation is float:
                            args.append(0.0)  # Default float
                        elif param.annotation is str:
                            args.append("TEST INPUT")  # Default string
                        else:
                            args.append(None)  # Default fallback

                    await attr(*args)

    """
        async def _screen_demo(self):
            await self.lcd.message(
                "",
                "",
                "",
                "",
                #display_time=0.1,
            )
    """
