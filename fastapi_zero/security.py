from datetime import UTC, datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import TokenData
from fastapi_zero.settings import Settings

config = Settings()
pwd_context = PasswordHash.recommended()
SECRET_KEY = config.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITOMO = config.ALGORITOMO
route_auth = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):
    to_enconde = data.copy()
    exp = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({'exp': exp})
    encode_jwt = encode(to_enconde, SECRET_KEY, algorithm=ALGORITOMO)
    return encode_jwt


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(route_auth)
):
    credentials_erro = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Problema para autenticar usuario',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        dados_token = decode(token, SECRET_KEY, algorithms=[ALGORITOMO])
        username: str = dados_token.get('sub')
        if not username:
            raise credentials_erro
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_erro
    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if not user:
        raise credentials_erro
    return user


def get_password_hash(password: str):
    return pwd_context.hash(password=password)


def verify_password(password_puro: str, password_hashed: str):
    return pwd_context.verify(password=password_puro, hash=password_hashed)
