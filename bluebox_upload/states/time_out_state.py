from states.base_state import State
from app_context import AppContext


class TimeOutState(State):
    async def run(self, context: AppContext) -> State:
        from states.waiting_for_card import WaitingForCardState

        context.flags.lcd_in_use = True
        await context.screens.session_ended_by_timeout()
        context.flags.lcd_in_use = False

        return WaitingForCardState()
