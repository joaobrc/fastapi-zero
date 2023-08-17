def test_retorna_code_200(cliente):
    resposta = cliente.get('/')
    assert resposta.status_code == 200
    assert resposta.json() == {'message': 'Olá Mundo'}


def test_criacao_de_usuario_retorna_201(cliente):
    resposta = cliente.post(
        url='/user/',
        json={
            'username': 'joao',
            'email': 'joao@local.com',
            'password': '123456',
        },
    )
    assert resposta.status_code == 201
    assert resposta.json() == {
        'id': 1,
        'username': 'joao',
        'email': 'joao@local.com',
    }
