from states.base_state import State
from app_context import AppContext
from states.waiting_for_card import WaitingForCardState
from networking import fetch_ip, fetch_mac
from model_classes import Instrument, Token
from networking import safe_api_call, check_internet_connection
from token_handler import verify_token


class InitState(State):
    """
    Initialize application.
    Verify token (or request new one).
    Fetch Instrument data.
    """

    async def run(self, context: AppContext) -> State:
        await context.screens.starting_screen()
        context.network_status = await check_internet_connection()

        token: Token = await safe_api_call(
            lambda: verify_token(),
            context=context,
            api_screens=context.screens,
            logger=context.logger,
        )

        if token:
            context.token = token
        else:
            return self

        ip = await fetch_ip()
        mac = await fetch_mac()

        instrument: Instrument = await safe_api_call(
            context.api.fetch_instrument_data,
            context=context,
            api_screens=context.screens,
            # api parameters
            mac=mac,
            ip=ip,
        )

        if instrument:
            context.instrument = instrument
        else:
            return self
        return WaitingForCardState()
