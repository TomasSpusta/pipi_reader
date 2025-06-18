# states/init_state.py
from states.base_state import State
from app_context import AppContext
from states.waiting_for_card import WaitingForCardState
from networking import fetch_ip, fetch_mac
from model_classes import Instrument, Token
from states.offline_state import OfflineState


class InitState(State):
    async def run(self, context: AppContext) -> State:
        await context.screens.starting_screen()

        token: Token = await context.api.fetch_token()
        if token:
            context.token = token
        else:
            return OfflineState()

        ip = await fetch_ip()
        mac = await fetch_mac()

        instrument: Instrument = await context.api.fetch_instrument_data(mac, ip)
        if instrument:
            context.instrument = instrument
        else:
            return OfflineState()

        print("going to WaitForCard")
        return WaitingForCardState()
