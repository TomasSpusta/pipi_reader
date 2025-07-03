import asyncio
import contextlib
from states.base_state import State
from app_context import AppContext
from button_handler import multi_button_watcher
from networking import safe_api_call, check_internet_connection


class TestState(State):
    async def run(self, context: AppContext) -> State:
        context.network_status = await check_internet_connection()
        state_queue = asyncio.Queue()
        asyncio.create_task(multi_button_watcher(context, state_queue))

        """
        print("🧪 TestState: Monitoring buttons with new logic.")

        INACTIVITY_LIMIT = 8  # seconds
        last_press_time = asyncio.get_running_loop().time()

        # Dummy screen placeholders
        async def fake_end_session_screen():
            print("🖥️ Prompt: Do you want to end the session?")
            nonlocal last_press_time
            last_press_time = asyncio.get_running_loop().time()

        async def fake_extend_session_screen():
            print("🖥️ Prompt: Do you want to extend the session?")
            nonlocal last_press_time
            last_press_time = asyncio.get_running_loop().time()

        async def fake_session_ended():
            nonlocal last_press_time
            print("✅ Action: Session ended by user.")
            last_press_time = asyncio.get_running_loop().time()

        async def fake_session_extended():
            nonlocal last_press_time
            print("✅ Action: Session extended.")
            last_press_time = asyncio.get_running_loop().time()

        # Inject dummy screens for testing
        context.screens.want_to_end_session = fake_end_session_screen
        context.screens.want_to_extend_reservation = fake_extend_session_screen
        context.screens.user_stop_reservation = fake_session_ended
        context.screens.reservation_extended = fake_session_extended

        # Launch button monitoring
        button_task = asyncio.create_task(handling_buttons(context))

        try:
            while True:
                await asyncio.sleep(0.5)
                now = asyncio.get_running_loop().time()
                if now - last_press_time >= INACTIVITY_LIMIT:
                    print(
                        f"⏳ No button activity for {INACTIVITY_LIMIT} sec. Returning to TestState."
                    )
                    break
        finally:
            button_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await button_task
        return self
        """
