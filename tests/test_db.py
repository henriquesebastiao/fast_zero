from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='hick', email='hick@email.com', password='senhasegura'
    )

    session.add(user)
    session.commit()  # Faz a persistência no DB.

    result = session.scalar(select(User).where(User.email == 'hick@email.com'))

    assert result.username == 'hick'
