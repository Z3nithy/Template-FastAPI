import pytest
from pydantic import ValidationError

from core.config import Settings


def test_settings_load_environment_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("SECRET_KEY", "s" * 32)
    monkeypatch.setenv("ALGORITHM", "HS512")
    monkeypatch.setenv("DEBUG", "true")
    settings = Settings(_env_file=None)

    assert settings.database_url == "sqlite:///:memory:"
    assert settings.algorithm == "HS512"
    assert settings.debug is True


def test_settings_require_secret_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_settings_reject_short_secret_key() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, secret_key="short")
