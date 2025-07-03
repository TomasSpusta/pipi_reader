from app_context import AppContext, AppState
from screen_manager import Screens
import asyncio
from bluebox_upload.delete_state_utils import transition_to
from typing import Optional
from logger import Logger


class NetworkGuard:
    def __init__(self, network_status: dict, screens: Screens, app_context: AppContext):
        self.network_status = network_status
        self.screens = screens
        self.app_context = app_context

    async def ensure_online(self):
        if self.network_status["online"]:
            return

        self.app_context.flags.lcd_in_use = True
        self.app_context.flags.block_buttons = True
        transition_to(self.app_context, AppState.OFFLINE)
        await self.screens.no_connection()

        while not self.network_status["online"]:
            await asyncio.sleep(2)

        self.app_context.flags.lcd_in_use = False
        self.app_context.flags.screen_needs_refresh = True
        self.app_context.flags.block_buttons = False
        await self.screens.connection_restored()

        if (
            self.app_context.reservation
            and not self.app_context.reservation.ended_by_user
        ):
            transition_to(self.app_context, AppState.IN_SESSION)
        elif self.app_context.user:
            transition_to(self.app_context, AppState.STARTING_SESSION)
        elif self.app_context.instrument:
            transition_to(self.app_context, AppState.WAITING_FOR_CARD)
        else:
            transition_to(self.app_context, AppState.INIT)

    async def safe_api_call(
        self, api_func, *, logger: Optional[Logger] = None, **kwargs
    ):
        await self.ensure_online()
        try:
            return await api_func()
        except Exception as e:
            error_message = f"Error in {api_func.__name__}:{e}"
            print(error_message)
            if logger:
                await logger.write_log(12, error_message)
            await self.screens.error_message(str(e), source_function=api_func.__name__)
            return None
