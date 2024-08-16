from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import create_access_token, verify_password

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
    # Procura um usuário na base de dados com o email informado
    user = session.scalar(select(User).where(User.email == form_data.username))

    # Caso o usuário não exista ou a senha esteja errada, retorna um erro
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    # Caso tudo funcione um token JWT é criado
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
