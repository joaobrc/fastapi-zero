from fastapi import FastAPI, HTTPException
from fastapi_zero.schemas import UserPrivate, UserPublic, UserDB, UserList

app = FastAPI()

database = []


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo'}


@app.post('/user/', status_code=201, response_model=UserPublic)
def create_user(user: UserPrivate):
    usuario_com_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(usuario_com_id)
    return usuario_com_id


@app.get('/users/', status_code=200, response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserPrivate):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='Usuario nao encontrado')
    user_com_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_com_id
    return user_com_id
