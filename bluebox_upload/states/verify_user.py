from states.base_state import State
from app_context import AppContext
from model_classes import User
from networking import safe_api_call
from datetime import datetime


class VerifyUserState(State):
    async def run(self, context: AppContext) -> State:
        from states.verify_reservation import VerifyReservationState
        from states.waiting_for_card import WaitingForCardState

        await context.screens.checking_user()

        user: User = await safe_api_call(
            context.api.fetch_user_data,
            context=context,
            api_screens=context.screens,
            # api parameters
            card_id=context.card_id,
        )
        await context.logger.insert_new_row()
        await context.logger.make_log.log_entry(datetime.now())
        await context.logger.make_log.token(context.token.expiration)

        if user:
            context.user = user
            await context.logger.make_log.user_info(context.user.full_name)
            return VerifyReservationState()
        else:
            await context.screens.user_not_in_database()
            await context.logger.make_log.user_info(context.card_id)
            return WaitingForCardState()
