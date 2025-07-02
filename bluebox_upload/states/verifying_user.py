# 4. states/verifying_user.py
from states.base_state import State
from app_context import AppContext
from model_classes import User
from networking import safe_api_call


class VerifyingUserState(State):
    async def run(self, context: AppContext) -> State:
        from states.starting_session import StartingSessionState
        from states.waiting_for_card import WaitingForCardState

        await context.screens.checking_user()

        user: User = await safe_api_call(
            context.api.fetch_user_data,
            context=context,
            api_screens=context.screens,
            # api parameters
            card_id=context.card_id,
        )

        if user:
            context.user = user
            return StartingSessionState()
        else:
            await context.screens.user_not_in_database()
            return WaitingForCardState()
