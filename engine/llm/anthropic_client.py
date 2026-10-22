from __future__ import annotations

import json
import threading
import time
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

import anthropic

from engine.llm.retry import (
    GenerationCancelled,
    LLMError,
    LLMFatalError,
    LLMRateLimitError,
    LLMOverloadedError,
    LLMContextLengthError,
)
from engine.llm.router import ModelConfig, ModelRouter
from engine.models.enums import ModelTier

logger = logging.getLogger(__name__)


# ── Pricing per model (USD per 1M tokens) ───────────────────
# Matched by substring, most specific first. Unknown models fall back to Sonnet.
_PRICING = (
    ("opus-5-5",   {"in": 4.0,  "out": 20.0}),
    ("sonnet-5-5", {"in": 2.0,  "out": 10.0}),
    ("haiku-5-5",  {"in": 0.10, "out": 0.50}),
    ("fable",      {"in": 10.0, "out": 50.0}),
    ("opus",       {"in": 5.0,  "out": 25.0}),   # Opus 5, 4.8, 4.7, 4.6
    ("sonnet-5",   {"in": 2.0,  "out": 10.0}),
    ("sonnet",     {"in": 3.0,  "out": 15.0}),   # Sonnet 4.6
    ("haiku",      {"in": 1.0,  "out": 5.0}),    # Haiku 4.5
)


def _get_pricing(model_name: str) -> dict:
    name = model_name.lower()
    for family, rates in _PRICING:
        if family in name:
            return rates
    return {"in": 2.0, "out": 10.0}


# ── Model capability gates ──────────────────────────────────
# Haiku 4.5 and older reject output_config.effort with a 400.
_ACCEPTS_EFFORT = ("opus-4-6", "opus-4-7", "opus-4-8", "opus-5", "sonnet-4-6",
                   "sonnet-5", "haiku-5", "fable-5")

# Models that take server-side refusal fallbacks (`fallbacks: "default"`).
# A declined request is re-run on Anthropic's recommended model in the same call.
_ACCEPTS_FALLBACKS = ("opus-5", "sonnet-5-5", "fable-5")
_FALLBACK_BETA = "server-side-fallback-2026-07-01"


def _accepts_effort(model_name: str) -> bool:
    name = model_name.lower()
    return any(m in name for m in _ACCEPTS_EFFORT)


def _accepts_fallbacks(model_name: str) -> bool:
    name = model_name.lower()
    return any(m in name for m in _ACCEPTS_FALLBACKS)


@dataclass
class LLMResponse:
    """Structured response from an LLM call."""

    content: str
    model: str
    tokens_in: int
    tokens_out: int
    tokens_thinking: int
    time_s: float
    stop_reason: str
    thinking: str = ""
    # One entry per model that ran (more than one when a fallback took over).
    attempts: list[dict] = field(default_factory=list)

    @property
    def as_json(self) -> dict:
        """Parse content as JSON. Raises ValueError if invalid."""
        text = self.content.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[-1].strip() == "```":
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            text = "\n".join(lines).strip()
        return json.loads(text)


@dataclass
class UsageTracker:
    """Track cumulative token usage and cost across a pipeline run."""

    total_tokens_in: int = 0
    total_tokens_out: int = 0
    total_tokens_thinking: int = 0
    total_calls: int = 0
    total_time_s: float = 0.0
    calls: list[dict] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record(self, response: LLMResponse, task_label: str = ""):
        attempts = response.attempts or [{
            "model": response.model,
            "tokens_in": response.tokens_in,
            "tokens_out": response.tokens_out,
        }]
        with self._lock:
            self.total_tokens_in += response.tokens_in
            self.total_tokens_out += response.tokens_out
            self.total_tokens_thinking += response.tokens_thinking
            self.total_calls += 1
            self.total_time_s += response.time_s
            for a in attempts:
                self.calls.append({
                    "task": task_label,
                    "model": a["model"],
                    "tokens_in": a["tokens_in"],
                    "tokens_out": a["tokens_out"],
                    "tokens_thinking": response.tokens_thinking if a is attempts[-1] else 0,
                    "time_s": round(response.time_s, 2),
                })

    @property
    def total_cost_usd(self) -> float:
        total = 0.0
        with self._lock:
            calls = list(self.calls)
        for call in calls:
            rates = _get_pricing(call["model"])
            total += call["tokens_in"] * rates["in"] / 1e6
            total += call["tokens_out"] * rates["out"] / 1e6
            # Thinking tokens billed at output rate
            total += call["tokens_thinking"] * rates["out"] / 1e6
        return total

    def summary(self) -> str:
        parts = (
            f"{self.total_calls} calls | "
            f"{self.total_tokens_in:,} in + {self.total_tokens_out:,} out"
        )
        if self.total_tokens_thinking:
            parts += f" + {self.total_tokens_thinking:,} thinking"
        parts += f" | ${self.total_cost_usd:.3f} | {self.total_time_s:.1f}s"
        return parts


class AnthropicClient:
    """Wrapper around the Anthropic SDK with streaming, retry, routing, and usage tracking.

    `cancel_event`, when set by another thread, stops the run: the next call (or
    the one currently streaming) raises GenerationCancelled.
    """

    def __init__(
        self,
        api_key: str,
        router: ModelRouter,
        retry_config: Optional[dict] = None,
        cancel_event: Optional[threading.Event] = None,
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.router = router
        self.usage = UsageTracker()
        self.cancel_event = cancel_event or threading.Event()

        rc = retry_config or {}
        self._max_retries = rc.get("max_retries", 4)
        self._base_delay = rc.get("base_delay", 2.0)
        self._max_delay = rc.get("max_delay", 60.0)

    def call(
        self,
        system: str,
        user_message: str,
        model_config: Optional[ModelConfig] = None,
        tier: Optional[ModelTier] = None,
        task: Optional[str] = None,
        task_label: str = "",
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Make a single LLM call via streaming."""

        if model_config:
            config = model_config
        elif tier:
            config = self.router.get_config(tier)
        elif task:
            config = self.router.resolve(task=task)
        else:
            config = self.router.get_config(ModelTier.MEDIUM)

        final_max_tokens = max_tokens or config.max_tokens

        response = self._call_with_retry(
            model=config.model_name,
            system=system,
            user_message=user_message,
            max_tokens=final_max_tokens,
            thinking=config.thinking,
            effort=config.effort,
        )

        self.usage.record(response, task_label=task_label)
        return response

    def call_json(
        self,
        system: str,
        user_message: str,
        **kwargs: Any,
    ) -> dict:
        """Call and parse response as JSON."""
        response = self.call(system=system, user_message=user_message, **kwargs)
        return response.as_json

    def _check_cancelled(self) -> None:
        if self.cancel_event.is_set():
            raise GenerationCancelled()

    def _sleep(self, delay: float) -> None:
        """Back off, but wake up at once if the run is cancelled."""
        if self.cancel_event.wait(delay):
            raise GenerationCancelled()

    def _call_with_retry(
        self,
        model: str,
        system: str,
        user_message: str,
        max_tokens: int,
        thinking: Optional[dict] = None,
        effort: Optional[str] = None,
    ) -> LLMResponse:
        """Streaming API call with configurable retry.

        Transient errors (rate limit, overload, network) are retried with backoff.
        If they persist past the last retry the run stops with LLMFatalError, so
        the user can resume later instead of collecting a string of failed docs.
        """

        last_error: Optional[LLMError] = None
        for attempt in range(self._max_retries + 1):
            self._check_cancelled()
            try:
                return self._call_api(
                    model, system, user_message,
                    max_tokens, thinking, effort,
                )

            except (LLMRateLimitError, LLMOverloadedError) as e:
                last_error = e
                if attempt == self._max_retries:
                    break

                if isinstance(e, LLMRateLimitError) and e.retry_after:
                    delay = e.retry_after
                else:
                    delay = min(self._base_delay * (2 ** attempt), self._max_delay)

                logger.warning(
                    f"Retriable error (attempt {attempt + 1}/{self._max_retries}), "
                    f"retrying in {delay:.1f}s: {e}"
                )
                self._sleep(delay)

            except LLMFatalError:
                raise

            except LLMError as e:
                if not e.retriable:
                    raise
                last_error = e
                if attempt == self._max_retries:
                    break

                delay = min(self._base_delay * (2 ** attempt), self._max_delay)
                logger.warning(
                    f"Retriable error (attempt {attempt + 1}/{self._max_retries}), "
                    f"retrying in {delay:.1f}s: {e}"
                )
                self._sleep(delay)

        if isinstance(last_error, LLMRateLimitError):
            raise LLMFatalError("rate_limited", str(last_error), status_code=429)
        if isinstance(last_error, LLMOverloadedError):
            raise LLMFatalError("overloaded", str(last_error), status_code=last_error.status_code)
        if last_error is not None and last_error.status_code is None:
            raise LLMFatalError("network", str(last_error))
        raise last_error or LLMError("Max retries exceeded", retriable=False)

    def _call_api(
        self,
        model: str,
        system: str,
        user_message: str,
        max_tokens: int,
        thinking: Optional[dict] = None,
        effort: Optional[str] = None,
    ) -> LLMResponse:
        """Single streaming API call (no retry). Handles thinking blocks."""

        start = time.time()

        # ── Build API kwargs ──
        api_kwargs = dict(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user_message}],
        )

        if effort and _accepts_effort(model):
            api_kwargs["output_config"] = {"effort": effort}

        if thinking:
            api_kwargs["thinking"] = thinking

        if _accepts_fallbacks(model):
            api_kwargs["fallbacks"] = "default"
            api_kwargs["betas"] = [_FALLBACK_BETA]
            stream_fn = self.client.beta.messages.stream
        else:
            stream_fn = self.client.messages.stream

        try:
            collected_thinking = []

            with stream_fn(**api_kwargs) as stream:
                for event in stream:
                    if self.cancel_event.is_set():
                        raise GenerationCancelled()
                    if getattr(event, "type", None) != "content_block_delta":
                        continue
                    delta = event.delta
                    if getattr(delta, "thinking", None):
                        collected_thinking.append(delta.thinking)

                final_message = stream.get_final_message()

        except anthropic.AuthenticationError as e:
            raise LLMFatalError("invalid_api_key", str(e), status_code=401)

        except anthropic.PermissionDeniedError as e:
            raise LLMFatalError("permission_denied", str(e), status_code=403)

        except anthropic.NotFoundError as e:
            raise LLMFatalError("model_not_found", f"{model}: {e}", status_code=404)

        except anthropic.RateLimitError as e:
            retry_after = None
            if getattr(e, "response", None) is not None:
                retry_after_header = e.response.headers.get("retry-after")
                if retry_after_header:
                    try:
                        retry_after = float(retry_after_header)
                    except ValueError:
                        pass
            raise LLMRateLimitError(str(e), retry_after=retry_after)

        except (anthropic.InternalServerError, anthropic.OverloadedError,
                anthropic.ServiceUnavailableError) as e:
            raise LLMOverloadedError(str(e))

        except anthropic.BadRequestError as e:
            error_msg = str(e).lower()
            if "credit balance" in error_msg:
                raise LLMFatalError("no_credits", str(e), status_code=400)
            if "usage limit" in error_msg:
                raise LLMFatalError("spend_limit", str(e), status_code=400)
            if "context length" in error_msg or "too many tokens" in error_msg:
                raise LLMContextLengthError(str(e))
            raise LLMError(str(e), status_code=400, retriable=False)

        except anthropic.APIStatusError as e:
            status = getattr(e, "status_code", None)
            from engine.llm.retry import RETRIABLE_STATUS_CODES
            retriable = status in RETRIABLE_STATUS_CODES if status else False
            raise LLMError(str(e), status_code=status, retriable=retriable)

        except (anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
            # Retried; becomes a fatal "network" error once retries run out.
            raise LLMError(f"Connection error: {e}", status_code=None, retriable=True)

        elapsed = time.time() - start
        # After a mid-stream fallback the content holds the declined partial,
        # a `fallback` marker, then the fallback model's continuation. The text
        # blocks read in order form the complete answer.
        content = "".join(
            block.text for block in final_message.content
            if getattr(block, "type", None) == "text"
        )
        thinking_text = "".join(collected_thinking)
        usage = final_message.usage
        thinking_tokens = getattr(usage, "thinking_tokens", 0) or 0

        attempts = []
        for it in getattr(usage, "iterations", None) or []:
            if getattr(it, "type", None) in ("message", "fallback_message"):
                attempts.append({
                    "model": getattr(it, "model", None) or final_message.model,
                    "tokens_in": it.input_tokens,
                    "tokens_out": it.output_tokens,
                })

        result = LLMResponse(
            content=content,
            model=final_message.model,
            tokens_in=usage.input_tokens,
            tokens_out=usage.output_tokens,
            tokens_thinking=thinking_tokens,
            time_s=elapsed,
            stop_reason=final_message.stop_reason or "",
            thinking=thinking_text,
            attempts=attempts,
        )

        log_parts = (
            f"LLM call: model={result.model} "
            f"tokens={result.tokens_in}+{result.tokens_out}"
        )
        if thinking_tokens:
            log_parts += f"+{thinking_tokens} thinking"
        log_parts += f" time={elapsed:.1f}s stop={result.stop_reason}"
        logger.debug(log_parts)

        if result.stop_reason == "max_tokens":
            logger.warning(
                f"Response truncated (max_tokens={max_tokens}). "
                f"Output may be incomplete."
            )

        # Safety classifiers can decline a request. It comes back as HTTP 200
        # with empty/partial content, so it must be caught here rather than in
        # the except blocks above. With fallbacks on, this only happens when
        # the fallback model declined too.
        if result.stop_reason == "refusal":
            raise LLMError(
                f"Model {result.model} declined the request "
                f"(stop_reason=refusal, {len(content)} chars returned)",
                status_code=200,
                retriable=False,
            )

        return result
