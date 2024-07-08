from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    Token,
    UserList,
    UserPrivate,
    UserPublic,
)
from fastapi_zero.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user
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


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserPrivate, session: Session = Depends(get_session)):
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


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
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


@app.put(
    '/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def update_user(
    user_id: int, 
    user: UserPrivate, 
    session: Session = Depends(get_session), 
    current_user = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='User Sem autorização'
        )
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)
    return current_user


@app.delete(
    '/users/{user_id}', response_model=Message, status_code=HTTPStatus.OK
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)):
    session.delete(current_user)
    session.commit()
    return {'detail': 'Usuario Deletado'}
