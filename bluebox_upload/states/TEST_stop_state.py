from states.base_state import State
from app_context import AppContext
import asyncio


class StopState(State):
    async def run(self, context: AppContext) -> State:
        from states.TEST_counting_state import CountingState

        # await context.screens.loading_screen("Stopping...")

        async with context.lock:
            context.counter = 0
        await context.screens.show_stopped()
        await asyncio.sleep(1)
        return CountingState()
