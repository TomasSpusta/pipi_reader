import asyncio
from gpiozero import Button
from app_context import AppContext
from states.TEST_counting_state import CountingState
from screen_manager import Screens
from lcd_display import LCDController


async def test_main():
    context = AppContext()
    context.stop_btn = Button(21, pull_up=True, hold_time=0.05, bounce_time=0.05)
    context.extend_btn = Button(13, pull_up=True, hold_time=0.05, bounce_time=0.05)
    context.lock = asyncio.Lock()

    context.screens = Screens(LCDController())
    context.state = CountingState()

    while True:
        context.state = await context.state.run(context)


if __name__ == "__main__":
    try:
        asyncio.run(test_main())
    except KeyboardInterrupt:
        print("Shutting down")
