import asyncio
from states.base_state import State
from app_context import AppContext

from button_handler import button_watcher
import contextlib
from networking import safe_api_call
from states.time_out_state import TimeOutState


class InReservationState(State):
    async def run(self, context: AppContext) -> State:
        stop_btn = context.stop_btn
        extend_btn = context.extend_btn
        warning_time = 5  # warning in minutes
        state_queue = asyncio.Queue()

        watcher_task = asyncio.create_task(button_watcher(context, state_queue))

        try:
            while (
                context.reservation.remaining_time > 0
                and not context.reservation.ended_by_user
            ):
                try:
                    new_state = await state_queue.get_nowait()
                    return new_state
                except asyncio.QueueEmpty:
                    pass

                await context.screens.in_reservation(context.reservation.remaining_time)

                await safe_api_call(
                    context.api.fetch_recording_info,
                    context=context,
                    api_screens=context.screens,
                    # api parameters
                    token=context.token,
                    reservation=context.reservation,
                )
                await asyncio.sleep(0.5)

                if (
                    context.reservation.remaining_time <= warning_time
                    and not context.reservation.warning_sent
                    and not context.reservation.ended_by_user
                ):
                    await context.screens.reservation_end_warning(
                        context.reservation.remaining_time
                    )
                    context.reservation.warning_sent = True

        finally:
            watcher_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await watcher_task

        return TimeOutState()
