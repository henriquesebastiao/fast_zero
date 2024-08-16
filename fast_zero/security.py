from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import TokenData

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'your-secret-key'  # CHANGE-ME
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # Tentamos decodificar o token JWT usando a chave secreta
        # e o algoritmo especificado.
        # O token decodificado é armazenado na variável payload.
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extraímos o campo 'sub' (normalmente usado para armazenar o
        # identificador do usuário no token JWT)
        # e verificamos se ele existe.
        email: str = payload.get('sub')

        # Se não, lançamos a exceção credentials_exception.
        # Em seguida, criamos um objeto TokenData com o username.
        if not email:
            raise credentials_exception
        token_data = TokenData(username=email)
    except PyJWTError:
        raise credentials_exception
    user_db = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if not user_db:
        raise credentials_exception

    return user_db
