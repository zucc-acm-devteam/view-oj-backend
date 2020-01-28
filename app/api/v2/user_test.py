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


def test_get_user(client):
    # 获取已知用户
    assert get_user(client, 'admin')['data']['username'] == 'admin'
    # 获取不存在的用户
    assert get_user(client, '111')['code'] != 0


def test_create_user(client):
    # 未登录创建用户
    assert create_user(client, 'guest')['code'] != 0

    # 普通用户登录
    assert create_session(client, 'user', 'user')['code'] == 0
    # 普通用户创建用户
    assert create_user(client, 'guest')['code'] != 0

    # 管理员登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 管理员创建用户
    assert create_user(client, 'guest')['code'] == 0
    assert get_user(client, 'guest')['data']['username'] == 'guest'


def test_modify_user(client):
    # 未登录修改已知用户
    assert modify_user(client, 'user', nickname='123')['code'] != 0
    # 未登录修改不存在的用户
    assert modify_user(client, '111', nickname='123')['code'] != 0

    # 普通用户登录
    assert create_session(client, 'user', 'user')['code'] == 0
    # 修改当前用户
    assert modify_user(client, 'user', nickname='123')['code'] == 0
    assert get_user(client, 'user')['data']['nickname'] == '123'
    # 修改其他用户
    assert modify_user(client, 'admin', nickname='123')['code'] != 0
    # 修改不存在的用户
    assert modify_user(client, '111', nickname='123')['code'] != 0

    # 管理员登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 修改当前用户
    assert modify_user(client, 'admin', nickname='123')['code'] == 0
    assert get_user(client, 'admin')['data']['nickname'] == '123'
    # 修改其他用户
    assert modify_user(client, 'user', nickname='123')['code'] == 0
    assert get_user(client, 'user')['data']['nickname'] == '123'
    # 修改不存在的用户
    assert modify_user(client, '111', nickname='123')['code'] != 0


def test_search_user(client):
    # 搜索指定用户
    assert search_user(client, username='admin')['data']['data'][0]['username'] == 'admin'
    # 搜索不存在的用户
    assert search_user(client, username='888888888')['data']['data'] == []
