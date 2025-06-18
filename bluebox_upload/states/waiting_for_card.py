# 3. states/waiting_for_card.py
from states.base_state import State
from app_context import AppContext
from states.offline_state import OfflineState
#


class WaitingForCardState(State):
    async def run(self, context: AppContext) -> State:
        await context.rfid_reader.start()
        print("in wait for card")
        # for some reason program stucks here
        await context.screens.welcome_screen(context.instrument.name)
        """if context.instrument and context.instrument.name:
            await context.screens.welcome_screen(context.instrument.name)
        else:
            await context.screens.welcome_screen("Offline")
            return OfflineState()
        """

        print("waiting for card....")
        card_id = 0

        card_id = await context.rfid_reader.get_card()
        from states.verifying_user import VerifyingUserState

        if card_id:
            context.card_id = card_id
            await context.rfid_reader.stop()
            return VerifyingUserState()

        return self
