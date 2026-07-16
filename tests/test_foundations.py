import pytest
from app.models import AssistantConfig, AssistantKind, is_deterministic
from app.validate import validate_config
from app.errors import ConfigError


def make_cfg(**kw) -> AssistantConfig:
    base = dict(id="support", name="Support", kind=AssistantKind.SUPPORT,
                system_prompt="You are helpful.")
    base.update(kw)
    return AssistantConfig(**base)


def test_is_deterministic_threshold():
    assert is_deterministic(make_cfg(temperature=0.2)) is True
    assert is_deterministic(make_cfg(temperature=0.9)) is False


def test_validate_rejects_blank_id():
    with pytest.raises(ConfigError):
        validate_config(make_cfg(id="   "))


def test_validate_rejects_out_of_range_temperature():
    with pytest.raises(ConfigError):
        validate_config(make_cfg(temperature=5.0))


@pytest.mark.asyncio
async def test_safe_ask_returns_failure_on_error(monkeypatch):
    from app import service
    from app.errors import ModelCallError

    async def boom(cfg, message):
        raise ModelCallError("nope")

    monkeypatch.setattr(service, "ask", boom)
    res = await service.safe_ask(make_cfg(), "hi")
    assert res.ok is False
    assert "nope" in res.error
