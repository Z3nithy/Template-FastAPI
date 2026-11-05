from core.senha_hash import criar_hash_senha, verificar_senha


def test_password_hash_can_be_verified() -> None:
    password = "correct horse battery staple"
    password_hash = criar_hash_senha(password)

    assert password_hash != password
    assert verificar_senha(password, password_hash) is True
    assert verificar_senha("wrong password", password_hash) is False
