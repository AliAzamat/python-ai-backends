from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AssistantKind(str, Enum):
    """Exactly one of a fixed set — like a typed enum of roles."""
    SUPPORT = "support"
    OPERATIONS = "operations"
    INTERNAL = "internal"


@dataclass
class AssistantConfig:
    """The shape of one configured AI assistant."""
    id: str
    name: str
    kind: AssistantKind
    system_prompt: str
    temperature: float = 0.2          # a default — callers may omit it
    description: Optional[str] = None  # Optional[X] means "X or None"
    tools: list[str] = field(default_factory=list)


def is_deterministic(cfg: AssistantConfig) -> bool:
    """A low temperature means near-repeatable answers."""
    return cfg.temperature <= 0.3
