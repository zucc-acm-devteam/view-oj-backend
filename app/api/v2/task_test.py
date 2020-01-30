import json

from app.test_base import client


def create_session(client, username, password):
    res = client.post('/v2/session', json={
        'username': username,
        'password': password
    })
    return json.loads(res.data)


def create_task(client, **kwargs):
    res = client.post('/v2/task', json=kwargs)
    return json.loads(res.data)


def test_create_task(client):
    # 登录
    assert create_session(client, 'admin', 'admin')['code'] == 0
    # 创建单个craw_user_info任务
    assert create_task(client, type='craw_user_info', kwargs=json.dumps({
        'username': 'admin',
        'oj_id': 2
    }))['code'] == 0
    # 创建多个craw_user_info任务
    assert create_task(client, type='craw_user_info')['code'] == 0
    # 创建单个craw_problem_info任务
    assert create_task(client, type='craw_problem_info', kwargs=json.dumps({
        'problem_id': 1
    }))['code'] == 0
    # 创建单个calculate_user_rating任务
    assert create_task(client, type='calculate_user_rating', kwargs=json.dumps({
        'username': 'admin'
    }))['code'] == 0
    # 创建多个calculate_user_rating任务
    assert create_task(client, type='calculate_user_rating')['code'] == 0
