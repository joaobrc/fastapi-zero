from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_retorna_code_200(cliente):
    resposta = cliente.get('/')
    code = 200
    html = 'Ola mundo!'

    assert resposta.status_code == code
    assert html in resposta.text


def test_criacao_de_usuario_retorna_201(cliente):
    resposta = cliente.post(
        url='/users',
        json={
            'username': 'joao',
            'email': 'joao@local.com',
            'password': '123456',
        },
    )
    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.json() == {
        'id': 1,
        'username': 'joao',
        'email': 'joao@local.com',
    }


def test_erro_ao_criar_usuario_ja_cadastrado(cliente, user):
    resposta = cliente.post(
        url='/users',
        json={
            'username': 'teste',
            'email': 'joao@local.com',
            'password': 'joaasd',
        },
    )
    code = HTTPStatus.BAD_REQUEST
    assert resposta.status_code == code


def test_ler_os_usuarios_vazios_retorn_code_200(cliente):
    resposta = cliente.get('/users/')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'users': []}


def test_ler_os_usuarios_return_code_200(cliente, user):
    valida_user = UserPublic.model_validate(user).model_dump()
    requisicao = cliente.get('/users/')
    assert requisicao.json() == {'users': [valida_user]}


def test_retonar_um_usuario_cadastrado_e_code_200(cliente, user, token):
    valida_user = UserPublic.model_validate(user).model_dump()
    reposta = cliente.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert HTTPStatus.OK == reposta.status_code
    assert reposta.json() == valida_user


def test_atualizando_um_usuario_retornando_code_200(cliente, user, token):
    resposta = cliente.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'jb',
            'email': 'jb@local.com',
            'password': 'wwewqas',
        },
    )
    code = HTTPStatus.OK
    assert resposta.status_code == code
    assert resposta.json() == {
        'username': 'jb',
        'email': 'jb@local.com',
        'id': 1,
    }


def test_erro_ao_pegar_usuaaro_e_code_406(cliente, user, token):
    resposta = cliente.get('/users/32',
        headers={'Authorization': f'Bearer {token}'})
    code = HTTPStatus.UNAUTHORIZED
    assert resposta.status_code == code


def test_erro_ao_autualizar_retonando_code_406(cliente, user2, token):
    resposta = cliente.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fe',
            'email': 'fe@local.com',
            'password': 'retesde',
        },
    )
    code = HTTPStatus.UNAUTHORIZED
    assert resposta.status_code == code


def test_deletando_usuario_retonando_code_200(cliente, user, token):
    resposta = cliente.delete('/users/1',
        headers={'Authorization': f'Bearer {token}'})
    code = HTTPStatus.OK
    assert resposta.status_code == code
    assert resposta.json() == {'detail': 'Usuario Deletado'}


def test_erro_ao_deletar_e_retonandor_code_400(cliente):
    resposta = cliente.delete('/users/32')
    code = HTTPStatus.UNAUTHORIZED
    assert resposta.status_code == code


def test_adquirir_token_de_acess_teste_para_a_rota_token(cliente, user):
    resposta = cliente.post(
        '/token',
        data={'username': user.email, 'password': user.clear_password},
    )
    token = resposta.json()
    assert resposta.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_user_nao_encontrado(cliente):
    resposta = cliente.post(
        '/token',
        data={'username': 'joao@joao.com', 'password': 'teste3'}
    )
    assert resposta.status_code == HTTPStatus.BAD_REQUEST


def test_user_token_senha_invalida(cliente, user):
    resposta = cliente.post(
        'token',
        data={'username': user.email, 'password': 'Abc'}
    )
    assert resposta.status_code == HTTPStatus.BAD_REQUEST

def test_erro_de_usuario_com_email_ja_criado(cliente, user):
    resposta = cliente.post(
        '/users',
        json={
            'username': 'teste33',
            'email': 'teste@teste.com',
            'password': 'joaasd',
        })
    assert resposta.status_code == HTTPStatus.BAD_REQUEST
