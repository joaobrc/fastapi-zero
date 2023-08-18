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


def test_ler_os_usuarios__retorn_code_200(cliente):
    resposta = cliente.get('/users/')
    assert resposta.status_code == 200
    assert resposta.json() == {
        'users': [
            {
                'username': 'joao',
                'email': 'joao@local.com',
                'id': 1,
            }
        ]
    }


def test_atualizando_um_usuario_retornando_code_200(cliente):
    resposta = cliente.put(
        '/users/1',
        json={
            'username': 'jb',
            'email': 'jb@local.com',
            'password': 'wwewqas',
        },
    )
    assert resposta.status_code == 200
    assert resposta.json() == {
        'username': 'jb',
        'email': 'jb@local.com',
        'id': 1,
    }
