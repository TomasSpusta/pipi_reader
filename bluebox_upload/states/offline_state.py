# 7. states/offline_state.py
import asyncio
from states.base_state import State
from app_context import AppContext


class OfflineState(State):
    async def run(self, context: AppContext) -> State:
        from states.waiting_for_card_state import WaitingForCardState

        await context.screens.no_connection()
        while True:
            await asyncio.sleep(3)
            if await context.api.check_connection():
                await context.screens.connection_restored()
                return WaitingForCardState()
        return self
