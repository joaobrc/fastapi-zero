from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPrivate,
    UserPublic,
)

app = FastAPI()

database = []


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


@app.post('/user/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserPrivate):
    usuario_com_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(usuario_com_id)
    return usuario_com_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.get(
    '/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            detail='Usuario nao encontrado',
        )
    return database[user_id - 1]


@app.put('/user/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserPrivate):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            detail='Usuario nao encontrado',
        )
    user_com_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_com_id
    return user_com_id


@app.delete('/user/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Usuario nao encontrado'
        )
    del database[user_id - 1]
    return {'detail': 'Usuario Deletado'}
