from __future__ import annotations

import time
import logging
from functools import wraps
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar("T")

# ─── Anthropic-specific retriable errors ─────────────────────────

RETRIABLE_STATUS_CODES = {
    429,   # Rate limited
    529,   # Overloaded
    500,   # Internal server error
    502,   # Bad gateway (transient)
    503,   # Service unavailable
}


class LLMError(Exception):
    """Base error for LLM calls."""

    def __init__(self, message: str, status_code: int | None = None, retriable: bool = False):
        super().__init__(message)
        self.status_code = status_code
        self.retriable = retriable


class LLMRateLimitError(LLMError):
    """Rate limited — always retriable."""

    def __init__(self, message: str, retry_after: float | None = None):
        super().__init__(message, status_code=429, retriable=True)
        self.retry_after = retry_after


class LLMOverloadedError(LLMError):
    """API overloaded — retriable with longer backoff."""

    def __init__(self, message: str):
        super().__init__(message, status_code=529, retriable=True)


class LLMContextLengthError(LLMError):
    """Prompt too long — NOT retriable (must reduce context)."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400, retriable=False)


class LLMFatalError(LLMError):
    """An error every later call would hit too, so the whole run stops here.

    `code` is a stable identifier the app turns into a user-facing message:
    invalid_api_key, permission_denied, no_credits, spend_limit,
    model_not_found, rate_limited, overloaded, network.
    The run can be resumed once the cause is fixed.
    """

    def __init__(self, code: str, message: str, status_code: int | None = None):
        super().__init__(message, status_code=status_code, retriable=False)
        self.code = code


class GenerationCancelled(Exception):
    """The user cancelled the run. Raised between or during LLM calls."""


# Errors the pipeline must let through instead of recording a per-document failure.
ABORT_ERRORS = (LLMFatalError, GenerationCancelled)


# ─── Retry decorator ────────────────────────────────────────────

def retry_with_backoff(
    max_retries: int = 4,
    base_delay: float = 2.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
) -> Callable:
    """Retry decorator with exponential backoff for LLM calls.

    Respects Anthropic's retry-after header when available.
    Does NOT retry non-retriable errors (context length, auth, etc.).
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except LLMRateLimitError as e:
                    last_exception = e
                    if attempt == max_retries:
                        break

                    # Use retry-after if provided, otherwise backoff
                    if e.retry_after:
                        delay = e.retry_after
                    else:
                        delay = min(base_delay * (exponential_base ** attempt), max_delay)

                    logger.warning(
                        f"Rate limited (attempt {attempt + 1}/{max_retries + 1}), "
                        f"waiting {delay:.1f}s"
                    )
                    time.sleep(delay)

                except LLMOverloadedError as e:
                    last_exception = e
                    if attempt == max_retries:
                        break

                    # Overloaded gets longer backoff
                    delay = min(base_delay * (exponential_base ** (attempt + 1)), max_delay)
                    logger.warning(
                        f"API overloaded (attempt {attempt + 1}/{max_retries + 1}), "
                        f"waiting {delay:.1f}s"
                    )
                    time.sleep(delay)

                except LLMError as e:
                    if not e.retriable:
                        raise  # context length, auth errors — don't retry
                    last_exception = e
                    if attempt == max_retries:
                        break

                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    logger.warning(
                        f"Retriable error (attempt {attempt + 1}/{max_retries + 1}): {e}, "
                        f"waiting {delay:.1f}s"
                    )
                    time.sleep(delay)

            raise last_exception  # type: ignore

        return wrapper

    return decorator