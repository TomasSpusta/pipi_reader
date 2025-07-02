from typing import Callable, Optional, Any
from logger import Logger


async def safe_api_call(
    api_func: Callable[..., Any], *, context, logger: Optional[Logger] = None, **kwargs
) -> Optional[Any]:
    """
    Safely executes an API function, ensuring the device is online.
    Handles exceptions by showing messages on the screen.

    :param api_func: The API coroutine function to call.
    :param context: AppContext instance containing screens, network status, etc.
    :param logger: Optional logger to record errors.
    :param kwargs: Additional arguments for the API function.
    :return: Result from API or None if failed.
    """
    # Optionally wait until online
    if hasattr(context, "network_guard") and context.network_guard:
        await context.network_guard.ensure_online()

    try:
        return await api_func(**kwargs)
    except Exception as e:
        error_message = f"Error in {api_func.__name__}: {e}"
        print(error_message)

        if logger:
            await logger.write_log(12, error_message)

        await context.screens.error_message(str(e), source_function=api_func.__name__)
        return None
