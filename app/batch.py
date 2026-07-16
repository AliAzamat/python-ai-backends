import asyncio
from app.models import AssistantConfig


async def warm_up(cfg: AssistantConfig) -> str:
    """Pretend to call a slow model endpoint and return its reply."""
    # `await` yields control while we wait on the (fake) network.
    await asyncio.sleep(0.5)
    return f"{cfg.name} ready"


async def warm_up_all(configs: list[AssistantConfig]) -> list[str]:
    """Warm up many assistants concurrently, not one-at-a-time."""
    # Schedule every call, then await them together.
    results = await asyncio.gather(*(warm_up(c) for c in configs))
    return list(results)
