import json

from app.test_base import client


def create_session(client, username, password):
    res = client.post('/v2/session', json={
        'username': username,
        'password': password
    })
    return json.loads(res.data)


def search_accept_problem(client, **kwargs):
    res = client.get('/v2/accept_problem', json=kwargs)
    return json.loads(res.data)


def test_search_accept_problem(client):
    # 登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 搜索全部
    assert len(search_accept_problem(client)['data']['data']) == 2
    # 搜索admin
    assert len(search_accept_problem(client, username='admin')['data']['data']) == 1
    # 搜索时间段
    assert len(search_accept_problem(client, username='admin',
                                     start_date="2019-01-01", end_date="2019-01-01")['data']['data']) == 1
    # 搜索时间段
    assert len(search_accept_problem(client, username='admin',
                                     start_date="2018-12-31", end_date="2018-12-31")['data']['data']) == 0
    # 搜索时间段
    assert len(search_accept_problem(client, username='admin',
                                     start_date="2018-01-02", end_date="2018-01-02")['data']['data']) == 0
    # 排序
    assert search_accept_problem(client, order=json.dumps({
        'id': 'asc'
    }))['data']['data'][0]['id'] == 2
    # 排序
    assert search_accept_problem(client, order=json.dumps({
        'id': 'desc'
    }))['data']['data'][0]['id'] == 3
