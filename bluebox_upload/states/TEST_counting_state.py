from states.base_state import State
from app_context import AppContext
import asyncio
import contextlib
from button_watcher import button_watcher


class CountingState(State):
    async def run(self, context: AppContext) -> State:
        state_queue = asyncio.Queue()
        watcher_task = asyncio.create_task(button_watcher(context, state_queue))

        from states.TEST_stop_state import StopState
        from states.TEST_reset_state import ResetState
        from states.TEST_done_state import DoneState

        try:
            while True:
                try:
                    new_state = await asyncio.wait_for(state_queue.get(), timeout=0.5)
                    if new_state == "stop":
                        return StopState()
                    elif new_state == "reset":
                        return ResetState()
                except asyncio.TimeoutError:
                    pass

                if not context.button_lock.locked():
                    async with context.lock:
                        if context.counter <= 0:
                            return DoneState()
                        else:
                            await context.screens.counting_screen(context.counter)
                            context.counter -= 1

        finally:
            watcher_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await watcher_task
