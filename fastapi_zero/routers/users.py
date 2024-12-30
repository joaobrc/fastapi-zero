from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.models import User
from fastapi_zero.schemas import Message, UserList, UserPrivate, UserPublic
from fastapi_zero.security import (
    get_current_user,
    get_password_hash,
    get_session,
)

routers = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@routers.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserPrivate, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User already registered',
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already registered',
            )

    password_user = get_password_hash(password=user.password)
    db_user = User(
        username=user.username, password=password_user, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@routers.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: T_Session,
    skip: int = 0,
    limit: int = 100,
):
    user = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': user}


@routers.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Usuario não autorizado',
        )

    database = session.scalars(select(User).where(User.id == user_id)).first()

    return database


@routers.put(
    '/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def update_user(
    user_id: int,
    user: UserPrivate,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='User Sem autorização'
        )
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)
    return current_user


@routers.delete(
    '/{user_id}', response_model=Message, status_code=HTTPStatus.OK
)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='User Sem autorização'
        )
    session.delete(current_user)
    session.commit()
    return {'detail': 'Usuario Deletado'}
