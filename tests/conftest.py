import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry
from fastapi_zero.security import get_password_hash


@pytest.fixture()
def cliente(session):
    def get_session_override():
        return session

    with TestClient(app) as cliente:
        app.dependency_overrides[get_session] = get_session_override
        yield cliente
    app.dependency_overrides.clear()


@pytest.fixture()
def user(session):
    user = User(
        username='teste',
        password=get_password_hash('teste1'),
        email='teste@teste.com',
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clear_password = 'teste1'
    return user


@pytest.fixture()
def user2(session):
    user = User(
        username='testes',
        password=get_password_hash('teste3'),
        email='testes@teste.com',
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clear_password = 'teste3'
    return user


@pytest.fixture()
def token(cliente, user):
    resposta = cliente.post(
        '/token',
        data={'username': user.email, 'password': user.clear_password},
    )
    return resposta.json()['access_token']


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
