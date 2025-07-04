from states.base_state import State
from app_context import AppContext
import asyncio


class ResetState(State):
    async def run(self, context: AppContext) -> State:
        from states.TEST_counting_state import CountingState

        # await context.screens.loading_screen("Reloading...")

        async with context.lock:
            context.counter = 100
        await context.screens.show_reloaded()
        await asyncio.sleep(1)
        return CountingState()
