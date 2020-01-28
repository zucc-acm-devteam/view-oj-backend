import json

from app.test_base import client


def create_session(client, username, password):
    res = client.post('/v2/session', json={
        'username': username,
        'password': password
    })
    return json.loads(res.data)


def get_user(client, id_):
    res = client.get('/v2/user/{}'.format(id_))
    return json.loads(res.data)


def create_oj_username(client, **kwargs):
    res = client.post('/v2/oj_username', json=kwargs)
    return json.loads(res.data)


def test_create_oj_username(client):
    # 登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 查看
    assert get_user(client, 'admin')['data']['oj_username'][0]['oj_username'] is None
    # 创建
    assert create_oj_username(client, username='admin', oj_id=1, oj_username='123')['code'] == 0
    # 查看
    assert get_user(client, 'admin')['data']['oj_username'][0]['oj_username'] == '123'
    # 修改
    assert create_oj_username(client, username='admin', oj_id=1, oj_username='321')['code'] == 0
    # 查看
    assert get_user(client, 'admin')['data']['oj_username'][0]['oj_username'] == '321'
    # 删除
    assert create_oj_username(client, username='admin', oj_id=1, oj_username='')['code'] == 0
    # 查看
    assert get_user(client, 'admin')['data']['oj_username'][0]['oj_username'] is None

    # 修改不可修改的OJ
    assert create_oj_username(client, username='admin', oj_id=3, oj_username='123')['code'] != 0
