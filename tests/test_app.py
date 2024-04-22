def test_retorna_code_200(cliente):
    resposta = cliente.get('/')
    code = 200
    html = 'Ola mundo!'

    assert resposta.status_code == code
    assert html in resposta.text


def test_criacao_de_usuario_retorna_201(cliente):
    resposta = cliente.post(
        url='/user/',
        json={
            'username': 'joao',
            'email': 'joao@local.com',
            'password': '123456',
        },
    )
    code = 201
    assert resposta.status_code == code
    assert resposta.json() == {
        'id': 1,
        'username': 'joao',
        'email': 'joao@local.com',
    }


def test_ler_os_usuarios__retorn_code_200(cliente):
    resposta = cliente.get('/users/')
    code = 200
    assert resposta.status_code == code
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
        '/user/1',
        json={
            'username': 'jb',
            'email': 'jb@local.com',
            'password': 'wwewqas',
        },
    )
    code = 200
    assert resposta.status_code == code
    assert resposta.json() == {
        'username': 'jb',
        'email': 'jb@local.com',
        'id': 1,
    }


def test_retonar_um_usuario_cadastrado_e_code_200(cliente):
    reposta = cliente.get('/user/1')
    code = 200
    assert reposta.status_code == code

def test_erro_ao_pegar_usuaaro_e_code_406(cliente):
    resposta = cliente.get('/user/36')
    code = 406
    assert resposta.status_code == code


def test_erro_ao_autualizar_retonando_code_406(cliente):
    resposta = cliente.put(
        '/user/32',
        json={
            'username': 'fe',
            'email': 'fe@local.com',
            'password': 'retesde',
        },
    )
    code = 406
    assert resposta.status_code == code


def test_deletando_usuario_retonando_code_200(cliente):
    resposta = cliente.delete('/user/1')
    code = 200
    assert resposta.status_code == code
    assert resposta.json() == {'detail': 'Usuario Deletado'}


def test_erro_ao_deletar_e_retonandor_code_400(cliente):
    resposta = cliente.delete('/user/32')
    code = 400
    assert resposta.status_code == code
