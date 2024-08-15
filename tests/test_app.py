from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_return_ok_and_hello_world(client):
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olar mundo!'}


def test_hello_world_endpoint_text(client):
    response = client.get('/hello_world')
    assert response.status_code == HTTPStatus.OK
    assert 'Olá mundo' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': 'password',
            'email': 'test@user.com',
        },
    )

    # Validar UserPublic
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testuser',
        'email': 'test@user.com',
        'id': 1,
    }


# Exercício 1 Aula 5
def test_create_user_with_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': 'password',
            'email': 'test@email.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


# Exercício 2 Aula 5
def test_create_user_with_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test_user',
            'password': 'password',
            'email': 'test@user.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    respose = client.get('/users/')
    assert respose.status_code == HTTPStatus.OK
    assert respose.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    respose = client.get('/users/')
    assert respose.status_code == HTTPStatus.OK
    assert respose.json() == {'users': [user_schema]}


def test_get_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testuser',
        'email': 'test@user.com',
        'id': 1,
    }


def test_try_get_user_with_not_found_user(client):
    response = client.get('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'testuser2',
            'password': 'password2',
            'email': 'test2@user.com',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testuser2',
        'email': 'test2@user.com',
        'id': 1,
    }


def test_try_update_user_with_not_found_user(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'testuser3',
            'password': 'password3',
            'email': 'test3@user.com',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_user_delete(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_try_delete_user_with_not_found_user(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
