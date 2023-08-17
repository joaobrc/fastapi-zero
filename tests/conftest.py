import pytest
from fastapi.testclient import TestClient
from fastapi_zero.app import app


@pytest.fixture
def cliente():
    cliente = TestClient(app)
    return cliente
