import pytest
from fastapi import HTTPException

from core.jwt import criar_token_acesso, verificar_token_acesso


def test_access_token_round_trip() -> None:
    token = criar_token_acesso(42)

    assert verificar_token_acesso(token) == 42


def test_invalid_access_token_is_rejected() -> None:
    with pytest.raises(HTTPException) as error:
        verificar_token_acesso("not-a-valid-token")

    assert error.value.status_code == 401
