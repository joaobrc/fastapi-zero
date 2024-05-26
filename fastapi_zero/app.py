from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserList,
    UserPrivate,
    UserPublic,
)

app = FastAPI()

@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def inicio():
    return """
        <html>
            <head></head>
            <body>
                <h1>Ola mundo!</h1>
            </body>
        </html>
"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserPrivate, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='User already registered',
        )
    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    user = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': user}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int, session: Session = Depends(get_session)):
    database = session.scalars(select(User).where(User.id == user_id)).first()
    if not database:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuario nao encontrado',
        )
    return database


@app.put('/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserPrivate, session: Session = Depends(get_session)):
    user_database = session.scalars(select(User).where(User.id == user_id)).first()
    if not user_database:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuario nao encontrado',
        )
    user_database.username = user.username
    user_database.password = user.password
    user_database.email = user.email
    session.commit()
    session.refresh(user_database)
    return user_database


@app.delete('/users/{user_id}', response_model=Message, status_code=HTTPStatus.OK)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_datebase = session.scalars(select(User).where(User.id == user_id)).first()
    if not user_datebase:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario nao encontrado'
        )
    session.delete(user_datebase)
    session.commit()
    return {'detail': 'Usuario Deletado'}
