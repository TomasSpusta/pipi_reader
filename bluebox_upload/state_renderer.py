from app_context import AppContext, AppState
from screen_manager import Screens


class StateRenderer:
    def __init__(self, screens: Screens):
        self.screens = screens

    async def render(self, context: AppContext):
        state = context.state

        if state == AppState.INIT:
            await self.screens.starting_screen()
        elif state == AppState.WAITING_FOR_CARD:
            if context.instrument:
                await self.screens.welcome_screen(context.instrument.name)

        elif state == AppState.VERIFYING_USER:
            await self.screens.checking_user()

        elif state == AppState.STARTING_SESSION:
            await self.screens.checking_reservation()

        elif state == AppState.IN_SESSION:
            if context.session:
                await self.screens.in_session(context.session.remaining_time)

        elif state == AppState.SESSION_ENDED:
            await self.screens.session_ended_by_timeout()

        elif state == AppState.OFFLINE:
            await self.screens.no_connection()

        elif state == AppState.RECOVERED:
            await self.screens.connection_restored()
