from http import HTTPStatus


def test_get_token(client, user):
    """
    Nesse teste, nós enviamos uma requisição POST
    para o endpoint "/token" com um username e uma senha válidos.
    Então, nós verificamos que a resposta contém um "access_token"
    e um "token_type", que são os campos que esperamos de um JWT válido.
    """
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
