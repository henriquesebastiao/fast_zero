from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from fast_zero.security import create_access_token, get_current_user
from fast_zero.settings import Settings

settings = Settings()


def test_jwt():
    data = {'sub': 'user@test.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']  # Testa se o valor de exp foi adicionado ao token


def test_jwt_invalid_token(client):
    """Testa a deleção de usuário com um token inválido"""
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_valid_token_with_user_not_exists(client, token):
    # Remove seu próprio usuário
    client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Agora tenta remove-lo de novo sendo que já não existe
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_without_sub():
    token = create_access_token(data={})

    with pytest.raises(HTTPException):
        get_current_user(token=token)
