from gpiozero import Button
from model_classes import Instrument, Session, Token, User
from screen_manager import Screens
import asyncio
import networking
from app_context import AppContext


async def handle_button_hold(
    btn: Button,
    prompt_shown: bool,
    prompt_func,
    action_func,
    hold_time: float = 3.0,
    timeout: float = 10.0,
    on_timeout: callable = None,
) -> bool:
    """
    Handles a hold action with an optional prompt and callback.
    Returns True if action was triggered, False otherwise.
    """
    if btn.is_pressed:
        if not prompt_shown:
            await prompt_func()
            prompt_shown = True

        prompt_start = asyncio.get_event_loop().time()

        while True:
            now = asyncio.get_event_loop().time()
            if now - prompt_start >= timeout:
                if on_timeout:
                    await on_timeout()
                return False

            if btn.is_pressed:
                hold_start = asyncio.get_event_loop().time()

                while btn.is_pressed:
                    if asyncio.get_event_loop().time() - hold_start >= hold_time:
                        await action_func()
                        return True
                    await asyncio.sleep(0.1)
                print("action cancelled")
                return False
            await asyncio.sleep(0.1)
    return False


async def buttons_handling(context: AppContext):
    stop_btn = context.stop_btn
    extend_btn = context.extend_btn
    session = context.session
    screens = context.screens

    token = context.token
    instrument = context.instrument
    user = context.user
    lcd_flags = context.flags
    network_status = context.network_status

    stop_prompt_shown = False
    extend_prompt_shown = False

    async def stop_reservation():
        nonlocal stop_prompt_shown
        print("stop reservation button hold")
        await networking.stop_recording(session, instrument, token)
        await screens.session_ended_by_user()
        session.ended_by_user = True
        lcd_flags.lcd_in_use = True

    async def extend_reservation():
        nonlocal extend_prompt_shown
        print("extend reservation button hold")
        await networking.start_recording(user, instrument, token)
        await screens.session_extended()
        lcd_flags.lcd_in_use = False
        extend_prompt_shown = False

    async def on_stop_timeout():
        lcd_flags.lcd_in_use = False
        await screens.returning()

    while session.remaining_time > 0 and not session.ended_by_user:
        if lcd_flags.block_input:
            await asyncio.sleep(0.5)
            continue

        if stop_btn.is_pressed:
            lcd_flags.lcd_in_use = True
            action_done = await handle_button_hold(
                stop_btn,
                stop_prompt_shown,
                screens.want_to_end_session,
                stop_reservation,
                on_timeout=on_stop_timeout,
            )
            stop_prompt_shown = not action_done
        else:
            stop_prompt_shown = False

        if extend_btn.is_pressed:
            lcd_flags.lcd_in_use = True
            if session.remaining_time < 15:
                action_done = await handle_button_hold(
                    extend_btn,
                    extend_prompt_shown,
                    screens.want_to_extend_session,
                    extend_reservation,
                    on_timeout=on_stop_timeout,
                )
                extend_prompt_shown = not action_done
            else:
                await screens.extend_not_yet()
                lcd_flags.lcd_in_use = False
        else:
            extend_prompt_shown = False

        await asyncio.sleep(0.1)
