import logging
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

import requests
from requests.exceptions import RequestException

# Use ParamSpec to perfectly forward the parameter types of the decorated function
P = ParamSpec("P")
T = TypeVar("T")


def handle_api_errors(
    logger: logging.Logger,
) -> Callable[[Callable[P, T]], Callable[P, T | None]]:
    """
    A decorator factory to handle API errors and logging consistently.

    It catches request-related errors and other exceptions, logs them,
    and returns None on failure.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T | None]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
            try:
                result = func(*args, **kwargs)
                # Log success after the call, regardless of the return value.
                logger.info(f"API call to '{func.__name__}' was successful.")
                return result
            except RequestException as e:
                # Specific handling for web request errors.
                logger.error(
                    f"API request failed in '{func.__name__}': {e}",
                    # exc_info=True adds the full traceback to the log record.
                    exc_info=True,
                )
                return None
            except Exception as e:
                # Catch-all for any other unexpected errors.
                logger.error(
                    f"An unexpected error occurred in '{func.__name__}': {e}",
                    exc_info=True,
                )
                return None

        return wrapper

    return decorator
