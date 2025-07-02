from gpiozero import Button
import asyncio
from networking import safe_api_call
from app_context import AppContext, AppFlags


async def handle_button_hold(
    btn: Button,
    prompt_shown: bool,
    prompt_func,  # screen which is shown when user presses button
    action_func,  # action when user holds button
    hold_time: float = 3.0,
    timeout: float = 8.0,
    on_timeout: callable = None,
    lcd_flags: AppFlags = None,
) -> bool:
    """
    Handles a hold action with an optional prompt and callback.
    Returns True if action was triggered, False otherwise.
    """
    if not btn.is_pressed:
        return False

    if not prompt_shown:
        if lcd_flags:
            lcd_flags.lcd_in_use = True
            await prompt_func()
            prompt_shown = True
    loop = asyncio.get_running_loop()
    prompt_start = loop.time()

    while True:
        print(f"Lcd in use:{lcd_flags.lcd_in_use}, in handle_button_hold loop.")
        now = loop.time()

        if now - prompt_start >= timeout:
            if lcd_flags:
                lcd_flags.lcd_in_use = False
            if on_timeout:
                await on_timeout()
            return False

        if btn.is_pressed:
            hold_start = loop.time()
            while btn.is_pressed:
                if loop.time() - hold_start >= hold_time:
                    if lcd_flags:
                        lcd_flags.lcd_in_use = False
                    await action_func()
                    return True
                await asyncio.sleep(0.2)

            if lcd_flags:
                lcd_flags.lcd_in_use = False
                print("Button hold canceled.")
                return False
        await asyncio.sleep(0.1)

        """
        
        
        
        
        
        
        # loop responsible to timeout from button screen to session screen
        print(f"Lcd in use:{lcd_flags.lcd_in_use}, in handle_button_hold loop.")
        now = asyncio.get_event_loop().time()
        if now - prompt_start >= timeout:
            if lcd_flags:
                lcd_flags.lcd_in_use = False
            if on_timeout:
                await on_timeout()
            return False

        if btn.is_pressed:
            hold_start = asyncio.get_event_loop().time()

            while btn.is_pressed:
                if asyncio.get_event_loop().time() - hold_start >= hold_time:
                    if lcd_flags:
                        lcd_flags.lcd_in_use = False
                    await action_func()
                    return True
                await asyncio.sleep(0.1)
            print("action cancelled")
            if lcd_flags:
                lcd_flags.lcd_in_use = False
            return False
        await asyncio.sleep(0.1)
        return False

"""


async def buttons_handling(context: AppContext):
    """_summary_

    Args:
        context (AppContext): _description_
    """

    stop_btn = context.stop_btn
    extend_btn = context.extend_btn
    session = context.session
    screens = context.screens

    token = context.token
    instrument = context.instrument
    user = context.user
    lcd_flags = context.flags
    # network_status = context.network_status

    stop_prompt_shown = False
    extend_prompt_shown = False

    async def stop_reservation():
        nonlocal stop_prompt_shown
        lcd_flags.lcd_in_use = True

        await safe_api_call(
            context.api.stop_recording,
            context=context,
            api_screens=screens,
            # api parameters
            session=session,
            instrument=instrument,
            token=token,
        )
        await screens.session_ended_by_user()
        print("Stop btn held")
        session.ended_by_user = True

    async def extend_reservation():
        nonlocal extend_prompt_shown
        lcd_flags.lcd_in_use = True

        await safe_api_call(
            context.api.start_recording,
            context=context,
            api_screens=screens,
            # api parameters
            user=user,
            instrument=instrument,
            token=token,
        )
        await screens.session_extended()
        print("Extend btn held")
        extend_prompt_shown = False

    async def on_stop_timeout():
        lcd_flags.lcd_in_use = False
        # await screens.returning()

    while session.remaining_time > 0 and not session.ended_by_user:
        if lcd_flags.block_buttons or lcd_flags.lcd_in_use:
            await asyncio.sleep(0.5)
            continue

        if stop_btn.is_pressed:
            print("Stop BTN pressed")
            action_done = await handle_button_hold(
                stop_btn,
                stop_prompt_shown,
                screens.want_to_end_session,
                stop_reservation,
                on_timeout=on_stop_timeout,
                lcd_flags=lcd_flags,
            )
            stop_prompt_shown = not action_done
        else:
            stop_prompt_shown = False

        if extend_btn.is_pressed:
            print("Extend BTN pressed")
            if session.remaining_time < 15:
                action_done = await handle_button_hold(
                    extend_btn,
                    extend_prompt_shown,
                    screens.want_to_extend_session,
                    extend_reservation,
                    on_timeout=on_stop_timeout,
                    lcd_flags=lcd_flags,
                )
                extend_prompt_shown = not action_done
            else:
                await screens.extend_not_yet()
                # lcd_flags.lcd_in_use = False
        else:
            extend_prompt_shown = False

        await asyncio.sleep(0.1)
