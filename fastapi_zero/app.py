from fastapi import FastAPI
from fastapi_zero.schemas import UserPrivate, UserPublic, UserDB

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
