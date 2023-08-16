from fastapi.testclient import TestClient
from fastapi_zero.app import app


def test_retorna_code_200():
    cliente = TestClient(app)
    resposta = cliente.get('/')
    assert resposta.status_code == 200
    assert resposta.json() == {'message': 'Olá Mundo'}
