# 5. states/starting_session.py
from states.base_state import State
from app_context import AppContext
from states.in_session import InSessionState


class StartingSessionState(State):
    async def run(self, context: AppContext) -> State:
        from states.waiting_for_card import WaitingForCardState

        await context.screens.checking_reservation()
        session = await context.api.start_recording(
            user=context.user, instrument=context.instrument, token=context.token
        )
        if session:
            context.session = session
            await context.screens.reservation_ok()
            return InSessionState()
        else:
            await context.screens.reservation_nok()
            return WaitingForCardState()
