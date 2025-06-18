# 5. states/starting_session.py
import asyncio
from states.base_state import State
from app_context import AppContext

# from states.waiting_for_card import WaitingForCardState
from button_handler import buttons_handling
import contextlib


class InSessionState(State):
    async def run(self, context: AppContext) -> State:
        from states.waiting_for_card import WaitingForCardState

        button_task = asyncio.create_task(buttons_handling(context))

        try:
            while (
                context.session.remaining_time > 0 and not context.session.ended_by_user
            ):
                await context.screens.in_session(context.session.remaining_time)
                await context.api.fetch_recording_info(context.token, context.session)
                await asyncio.sleep(5)
        finally:
            button_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await button_task
        return WaitingForCardState()  # tady bude muset byt endingSessionState
