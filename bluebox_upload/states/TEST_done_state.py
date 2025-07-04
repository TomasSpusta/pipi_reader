from states.base_state import State
from app_context import AppContext
import asyncio


class DoneState(State):
    async def run(self, context: AppContext) -> State:
        await context.screens.counter_done()
        return None
