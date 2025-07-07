from states.base_state import State
from app_context import AppContext
from datetime import datetime


class TimeOutState(State):
    async def run(self, context: AppContext) -> State:
        from states.waiting_for_card import WaitingForCardState

        async with context.lock:
            await context.screens.session_ended_by_timeout()
            await context.logger.write_log(11, datetime.now(), "Ended by timeout")

        return WaitingForCardState()
