import factory
import pytest
from factory.fuzzy import FuzzyChoice
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session  # Uma interface entre o código e o DB
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Todo, TodoState, User, table_registry
from fast_zero.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_user_{n}')

    # LazyAttribute é "preguiçoso", ele só cria o atributo email, após
    # o username ter sido criado, pois depende de saber dele.
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = FuzzyChoice(TodoState)
    user_id = 1


@pytest.fixture
def client(session):
    def test_session():
        return session

    with TestClient(app) as client:  # Arrange
        """
        Durante os testes, sobreescreve a sessão pela sessão do DB
        pelo DB em memória (test_session)
        """
        app.dependency_overrides[get_session] = test_session

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # Cria um pool de conexões com db.
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # Os testes não dependem dfas migrações do alembic.
    # As tabelas são criadas todas de uma vez.

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session: Session):
    password = 'password'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password  # Monkey Path

    # Retornamos a senha também em texto puro para a utilização no teste
    # test_get_token, pois lá para realizar o login, a senha em texto puro
    # deve ser eviada.

    # Monkey patching é uma técnica em que modificamos ou estendemos
    # o código em tempo de execução. Neste caso, estamos adicionando
    # um novo atributo clean_password ao objeto
    # user para armazenar a senha em texto puro.

    return user


@pytest.fixture
def other_user(session: Session):
    password = 'password'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
