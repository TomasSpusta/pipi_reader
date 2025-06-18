from app_context import AppContext, AppState
from typing import Optional
from state_renderer import StateRenderer
import asyncio


def transition_to(
    app_context: AppContext, new_state: AppState, renderer: Optional[StateRenderer]
):
    app_context.state = new_state
    print(f"[State] {new_state.name}")
    if renderer:
        asyncio.create_task(renderer.render(app_context))
