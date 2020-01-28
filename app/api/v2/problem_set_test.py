import json

from app.test_base import client


def create_session(client, username, password):
    res = client.post('/v2/session', json={
        'username': username,
        'password': password
    })
    return json.loads(res.data)


def get_problem_set(client, id_):
    res = client.get('/v2/problem_set/{}'.format(id_))
    return json.loads(res.data)


def create_problem_set(client, **kwargs):
    res = client.post('/v2/problem_set', json=kwargs)
    return json.loads(res.data)


def modify_problem_set(client, id_, **kwargs):
    res = client.patch('/v2/problem_set/{}'.format(id_), json=kwargs)
    return json.loads(res.data)


def delete_problem_set(client, id_):
    res = client.delete('/v2/problem_set/{}'.format(id_))
    return json.loads(res.data)


def test_get_problem_set(client):
    # 获取存在的题目集
    assert len(get_problem_set(client, 1)['data']['problem_list']) == 3
    # 获取不存在的题目集
    assert get_problem_set(client, 2)['code'] != 0


def test_create_problem_set(client):
    # 登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 创建题目集
    assert create_problem_set(client, name='test-problem-set',
                              problem_list=json.dumps(['hdu-1000', 'hdu-1001']))['code'] == 0
    # 获取题目集
    assert len(get_problem_set(client, 2)['data']['problem_list']) == 2


def test_modify_problem_set(client):
    # 登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 修改题目集
    assert modify_problem_set(client, 1, name='test-problem-set',
                              problem_list=json.dumps(['hdu-1000']))['code'] == 0
    # 获取题目集
    assert len(get_problem_set(client, 1)['data']['problem_list']) == 1
    # 修改不存在的题目集
    assert modify_problem_set(client, 99, name='test-problem-set',
                              problem_list=json.dumps(['hdu-1000']))['code'] != 0


def test_delete_problem_set(client):
    # 登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 删除题目集
    assert delete_problem_set(client, 1)['code'] == 0
    # 获取题目集
    assert get_problem_set(client, 1)['code'] != 0
