import json

from ...test_base import client


def get_session(client):
    res = client.get('/v2/session')
    return json.loads(res.data)


def create_session(client, username, password):
    res = client.post('/v2/session', json={
        'username': username,
        'password': password
    })
    return json.loads(res.data)


def delete_session(client):
    res = client.delete('/v2/session')
    return json.loads(res.data)


def test_session(client):
    # 获取登录状态
    assert get_session(client)['code'] != 0
    # 登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 获取登录状态
    assert get_session(client)['data']['username'] == 'admin'
    # 登出
    assert delete_session(client)['code'] == 0
    # 获取登录状态
    assert get_session(client)['code'] != 0
