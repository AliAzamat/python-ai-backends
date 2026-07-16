import asyncio
from openai import AsyncOpenAI, APITimeoutError, RateLimitError, APIError
from app.models import AssistantConfig
from app.errors import ModelCallError

# Reads OPENAI_API_KEY from the environment. Async client → awaitable calls.
client = AsyncOpenAI()

# These signal "try again later"; a bad request would not.
TRANSIENT = (APITimeoutError, RateLimitError)


async def ask(cfg: AssistantConfig, user_message: str, retries: int = 3) -> str:
    """Send one turn to the model, retrying transient failures with backoff."""
    for attempt in range(retries):
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=cfg.temperature,
                messages=[
                    {"role": "system", "content": cfg.system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            return response.choices[0].message.content or ""
        except TRANSIENT as exc:
            if attempt == retries - 1:
                raise ModelCallError(f"model call failed after {retries} tries") from exc
            # Exponential backoff: wait 1s, then 2s, then 4s...
            await asyncio.sleep(2 ** attempt)
        except APIError as exc:
            # Permanent (e.g. bad request) — don't retry, fail clearly.
            raise ModelCallError(f"model call rejected: {exc}") from exc
    raise ModelCallError("unreachable")  # pragma: no cover
