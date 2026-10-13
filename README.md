# Python for AI Backends

**The typed, async Python foundation for an AI assistant service: dataclass configs with enum kinds, invariant validation with domain exceptions, an async OpenAI client that retries only transient failures, a `Result` type for callers that must never crash, concurrent fan-out with `asyncio.gather`, and one-line JSON logging.**

These are the building blocks the follow-on [fastapi-service](https://github.com/AliAzamat/fastapi-service) project puts behind an HTTP API. Each module is small and focuses on one backend habit that matters once model calls are in the request path.

## Modules

| Module | What it shows |
|---|---|
| `app/models.py` | `AssistantConfig` dataclass (`id`, `name`, `kind`, `system_prompt`, `temperature` default 0.2, optional `description`, `tools`) and an `AssistantKind` string enum (`support`, `operations`, `internal`); `is_deterministic()` is true at temperature ≤ 0.3 |
| `app/validate.py` | Enforces invariants — non-blank id and prompt, temperature within [0, 2] — raising `ConfigError` |
| `app/llm.py` | Async OpenAI call that retries timeouts and rate limits with exponential backoff (1 s, 2 s, …) but fails immediately on permanent API errors, wrapping both in `ModelCallError` |
| `app/result.py` | Generic `Result[T]` with `success` / `failure` constructors and an `ok` property |
| `app/service.py` | `safe_ask()` — never raises; logs latency on success and the error on failure, returning a `Result` |
| `app/batch.py` | Warms up many assistants concurrently with `asyncio.gather` instead of one at a time |
| `app/logging_setup.py` | A JSON log formatter that merges structured `extra={"fields": …}` into each line |

## Example

```python
import asyncio
from app.models import AssistantConfig, AssistantKind
from app.validate import validate_config
from app.service import safe_ask

cfg = validate_config(AssistantConfig(
    id="support", name="Support Bot", kind=AssistantKind.SUPPORT,
    system_prompt="You are a concise product support agent.",
))

result = asyncio.run(safe_ask(cfg, "How do I reset my password?"))
print(result.value if result.ok else f"failed: {result.error}")
```

## Running the tests

Requires Python 3.10+.

```bash
git clone https://github.com/AliAzamat/python-ai-backends.git
cd python-ai-backends
pip install openai pytest pytest-asyncio

OPENAI_API_KEY=dummy python -m pytest -q   # 4 tests; the model call is mocked
```

`OPENAI_API_KEY` only needs to be set for the client to construct; the tests don't call the API.

## Notes

- There's no dependency file yet; `pytest-asyncio` is required for the async test.
- The tests cover the config invariants, the determinism threshold, and `safe_ask` turning a model failure into a `Result` — not the retry loop itself.
