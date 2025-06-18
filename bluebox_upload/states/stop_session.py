from states.base_state import State
from app_context import AppContext
from states.in_session import InSessionState
from button_handler import handle_button_hold
from states.waiting_for_card import WaitingForCardState


class StopSessionState(State):
    async def run(self, context: AppContext) -> State:
        await context.screens.want_to_end_session()

        async def stop_action():
            # if extend button held for 10 seconds -> api.start.recoding()
            await context.api.stop_recording(
                session=context.session,
                instrument=context.instrument,
                token=context.token,
            )
            await context.screens.session_ended_by_user()
            return WaitingForCardState

        async def timeout_action():
            await context.screens.returning()
            return InSessionState()

        await handle_button_hold(
            btn=context.stop_btn,
            prompt_shown=False,
            prompt_func=context.screens.want_to_end_session,
            action_func=stop_action,
            hold_time=10.0,
            timeout=12.0,
            on_timeout=timeout_action,
        )
