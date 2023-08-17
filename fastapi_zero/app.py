from fastapi import FastAPI
from fastapi_zero.schemas import UserPrivate, UserPublic

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo'}


@app.post('/user/', status_code=201, response_model=UserPublic)
def create_user(user: UserPrivate):
    return user
