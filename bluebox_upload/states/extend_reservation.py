# Extend session
from states.base_state import State
from app_context import AppContext

from networking import safe_api_call


class ExtendReservationState(State):
    """
    State dealing with extension of session/reservation.
    """

    async def run(self, context: AppContext) -> State:
        from states.in_reservation import InReservationState

        async with context.lock:
            if context.reservation.remaining_time > 15:
                await context.screens.extend_not_yet()
                return InReservationState()
            await safe_api_call(
                context.api.start_extend_reservation,
                context=context,
                api_screens=context.screens,
                # api variables:
                user=context.user,
                instrument=context.instrument,
                token=context.token,
            )
        await context.screens.reservation_extended()
        context.reservation.warning_sent = False
        # await asyncio.sleep(1)
        return InReservationState()

        """

        lcd_flags = context.flags
        lcd_flags.lcd_in_use = True

        if context.reservation.remaining_time > 15:
            await context.screens.extend_not_yet()
            lcd_flags.lcd_in_use = False
            return InReservationState()

        await context.screens.want_to_extend_reservation()
        held = await wait_for_button_hold(context.extend_btn)
        # lcd_flags = False ai put it here

        if held:
            await safe_api_call(
                context.api.start_extend_reservation,
                context=context,
                api_screens=context.screens,
                # api variables:
                user=context.user,
                instrument=context.instrument,
                token=context.token,
            )
            await context.screens.reservation_extended()
            lcd_flags.lcd_in_use = False
            return InReservationState()
        else:
            lcd_flags.lcd_in_use = False
            return InReservationState()
"""
