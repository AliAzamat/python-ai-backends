import logging
import time

from app.models import AssistantConfig
from app.llm import ask
from app.errors import ModelCallError
from app.result import Result

log = logging.getLogger("saep.service")


async def safe_ask(cfg: AssistantConfig, message: str) -> Result[str]:
    """Call the model but never raise: return a Result the caller inspects."""
    started = time.perf_counter()
    try:
        answer = await ask(cfg, message)
        elapsed_ms = (time.perf_counter() - started) * 1000
        log.info("ask ok", extra={"fields": {
            "assistant_id": cfg.id, "latency_ms": round(elapsed_ms, 1)}})
        return Result.success(answer)
    except ModelCallError as exc:
        log.warning("ask failed", extra={"fields": {
            "assistant_id": cfg.id, "error": str(exc)}})
        return Result.failure(str(exc))
