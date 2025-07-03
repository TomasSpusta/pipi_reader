from states.base_state import State
from app_context import AppContext


class WaitingForCardState(State):
    async def run(self, context: AppContext) -> State:
        await context.screens.welcome_screen(context.instrument.name)

        card_id = await context.rfid_reader.read_card()

        from states.verify_user import VerifyUserState

        if card_id:
            context.card_id = card_id
            return VerifyUserState()

        return self
