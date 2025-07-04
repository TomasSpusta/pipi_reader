from states.base_state import State
from app_context import AppContext


class TimeOutState(State):
    async def run(self, context: AppContext) -> State:
        from states.waiting_for_card import WaitingForCardState

        async with context.lock:
            await context.screens.session_ended_by_timeout()

        return WaitingForCardState()
