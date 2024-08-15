import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session  # Uma interface entre o código e o DB
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


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
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session: Session):
    user = User(
        username='testuser',
        password='password',
        email='test@user.com',
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
