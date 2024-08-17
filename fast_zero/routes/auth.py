from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])
T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

# A classe OAuth2PasswordRequestForm é uma classe especial do FastAPI
# que gera automaticamente um formulário para solicitar
# o username (email neste caso) e a senha.
# Este formulário será apresentado automaticamente no Swagger UI e Redoc,
# facilitando a realização de testes de autenticação.


@router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2Form,
):
    invalid_credentials_exception = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail='Incorrect email or password',
    )

    # Procura um usuário na base de dados com o email informado
    user = session.scalar(select(User).where(User.email == form_data.username))

    # Retorna um erro caso o usuário não exista
    if not user:
        raise invalid_credentials_exception
    # Retorna um erro caso a senha esteja errada
    elif not verify_password(form_data.password, user.password):
        raise invalid_credentials_exception

    # Caso tudo funcione um token JWT é criado
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
