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


def create_user(client, id_):
    res = client.post('/v2/user', json={
        'username': id_
    })
    return json.loads(res.data)


def modify_user(client, id_, **kwargs):
    res = client.patch('/v2/user/{}'.format(id_), json=kwargs)
    return json.loads(res.data)


def search_user(client, **kwargs):
    res = client.get('/v2/user', json=kwargs)
    return json.loads(res.data)


def test_user(client):
    # 普通用户登录
    assert create_session(client, 'user', 'user')['code'] == 0
    # 获取当前用户信息
    assert get_user(client, 'user')['data']['username'] == 'user'
    # 获取其他用户信息(reject)
    assert get_user(client, 'admin')['code'] != 0
    # 修改当前用户信息
    assert modify_user(client, 'user', nickname='user123')['code'] == 0
    # 获取当前用户信息
    assert get_user(client, 'user')['data']['nickname'] == 'user123'
    # 修改当前用户敏感信息(reject)
    assert modify_user(client, 'admin', status=1)['code'] != 0
    # 获取当前用户信息
    assert get_user(client, 'user')['data']['status'] == 0
    # 修改其他用户信息(reject)
    assert modify_user(client, 'admin', nickname='user123')['code'] != 0

    # 管理员登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 获取当前用户信息
    assert get_user(client, 'admin')['data']['username'] == 'admin'
    # 获取其他用户信息
    assert get_user(client, 'user')['data']['username'] == 'user'
    # 修改其他用户信息
    assert modify_user(client, 'user', nickname='user111')['code'] == 0
    # 获取其他用户信息
    assert get_user(client, 'user')['data']['nickname'] == 'user111'
    # 修改其他用户敏感信息
    assert modify_user(client, 'user', status=1)['code'] == 0
    # 获取其他用户信息
    assert get_user(client, 'user')['data']['status'] == 1
    # 获取所有用户信息
    assert len(search_user(client)['data']['data']) == 2
    # 创建用户
    assert create_user(client, 'guest')['code'] == 0
    # 获取创建的用户信息
    assert get_user(client, 'guest')['data']['nickname'] == 'guest'
    # 获取所有用户信息
    assert len(search_user(client)['data']['data']) == 3
