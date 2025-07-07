from states.base_state import State
from app_context import AppContext
from states.waiting_for_card import WaitingForCardState
from networking import safe_api_call


class UserStopReservationState(State):
    async def run(self, context: AppContext) -> State:
        async with context.lock:
            await safe_api_call(
                context.api.stop_reservation,
                context=context,
                api_screens=context.screens,
                # api variables:
                reservation=context.reservation,
                instrument=context.instrument,
                token=context.token,
            )
        await context.screens.user_stop_reservation()
        return WaitingForCardState()
