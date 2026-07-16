from app.models import AssistantConfig
from app.errors import ConfigError


def validate_config(cfg: AssistantConfig) -> AssistantConfig:
    """Check platform invariants; raise ConfigError on the first violation."""
    if not cfg.id.strip():
        raise ConfigError("id must be non-empty")
    if not cfg.system_prompt.strip():
        raise ConfigError("system_prompt must be non-empty")
    if not 0.0 <= cfg.temperature <= 2.0:
        raise ConfigError(f"temperature {cfg.temperature} out of range [0, 2]")
    return cfg
