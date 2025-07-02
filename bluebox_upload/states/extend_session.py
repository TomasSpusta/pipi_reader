# Extend session
from states.base_state import State
from app_context import AppContext
from states.in_session import InSessionState
from button_handler import handle_button_hold


class ExtendingSessionState(State):
    """
    State dealing with extension of session/reservation.
    """

    async def run(self, context: AppContext) -> State:
        if context.session.remaining_time > 15:
            await context.screens.extend_not_yet()
            return InSessionState()

        await context.screens.want_to_extend_session()

        async def extend_action():
            await context.api.start_recording(
                user=context.user, instrument=context.instrument, token=context.token
            )
            await context.screens.session_extended()
            return InSessionState()

        async def timeout_action():
            await context.screens.returning()
            return InSessionState()

        await handle_button_hold(
            btn=context.extend_btn,
            prompt_shown=False,
            prompt_func=context.screens.want_to_extend_session,
            action_func=extend_action,
            on_timeout=timeout_action,
        )
