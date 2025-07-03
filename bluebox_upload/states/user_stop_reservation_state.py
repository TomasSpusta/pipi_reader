from states.base_state import State
from app_context import AppContext

from button_handler import wait_for_button_hold
from states.waiting_for_card import WaitingForCardState
from networking import safe_api_call


class UserStopReservationState(State):
    async def run(self, context: AppContext) -> State:
        from states.in_reservation import InReservationState

        lcd_flags = context.flags
        lcd_flags.lcd_in_use = True
        await context.screens.want_to_end_session()
        held = await wait_for_button_hold(context.extend_btn)

        if held:
            await safe_api_call(
                context.api.stop_reservation,
                context=context,
                api_screens=context.screens,
                # api variables:
                user=context.user,
                instrument=context.instrument,
                token=context.token,
            )
            await context.screens.user_stop_reservation()
            lcd_flags.lcd_in_use = False
            return WaitingForCardState()
        else:
            lcd_flags.lcd_in_use = False
            return InReservationState()
