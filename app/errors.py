class ConfigError(ValueError):
    """Raised when an AssistantConfig violates a platform invariant."""


class ModelCallError(RuntimeError):
    """Raised when a model call fails after exhausting retries."""
