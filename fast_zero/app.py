from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, Token, UserList, UserPublic, UserSchema
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI()

fake_db = []  # Banco de dados falso


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olar mundo!'}


@app.get('/hello_world', response_class=HTMLResponse)
def hello_world():
    return """<div>Olá mundo</div>"""


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    # O método .add da sessão, adiciona o registro a sessão.
    # O dado fica em um estado transiente.
    # Ele não foi adicionado ao banco de dados ainda.
    # Mas já está reservado na sessão.
    # Ele é uma aplicação do padrão de projeto Unidade de trabalho.
    session.add(db_user)

    # No momento em que existem dados transientes na sessão
    # e queremos "performar" efetivamente as ações no banco de dados.
    # Usamos o método .commit.
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(session: Session = Depends(get_session)):
    users = session.scalars(select(User))
    return {'users': users}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


# O current_user define que o usuário deve estar logado
# para poder realizar a ação.


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user: UserSchema,
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Not enough permission'
        )

    current_user.email = user.email
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


# A classe OAuth2PasswordRequestForm é uma classe especial do FastAPI
# que gera automaticamente um formulário para solicitar
# o username (email neste caso) e a senha.
# Este formulário será apresentado automaticamente no Swagger UI e Redoc,
# facilitando a realização de testes de autenticação.


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
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
