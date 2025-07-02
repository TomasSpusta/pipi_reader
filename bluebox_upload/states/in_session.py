# 5. states/starting_session.py
import asyncio
from states.base_state import State
from app_context import AppContext
from button_handler import buttons_handling
import contextlib
from networking import safe_api_call
from states.time_out_session import TimeOutSessionState


class InSessionState(State):
    async def run(self, context: AppContext) -> State:
        # from states.waiting_for_card import WaitingForCardState

        button_task = asyncio.create_task(buttons_handling(context))

        try:
            while (
                context.session.remaining_time > 0 and not context.session.ended_by_user
            ):
                await context.screens.in_session(context.session.remaining_time)
                await safe_api_call(
                    context.api.fetch_recording_info,
                    context=context,
                    api_screens=context.screens,
                    # api parameters
                    token=context.token,
                    session=context.session,
                )
                await asyncio.sleep(5)
                warning_time = 5  # warning time in minutes
                if (
                    context.session.remaining_time <= warning_time
                    and not context.session.warning_sent
                    and not context.session.ended_by_user
                ):
                    await context.screens.session_end_warning(
                        context.session.remaining_time
                    )
                    context.session.warning_sent = True
        finally:
            button_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await button_task
        return TimeOutSessionState()
