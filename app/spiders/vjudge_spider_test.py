from app.spiders.vjudge_spider import VjudgeSpider
from app.test_base import client


def test_vjudge_user_info(client):
    from app import create_app
    from app.models.oj_username import OJUsername
    create_app().app_context().push()
    oj_username = OJUsername()
    oj_username.oj_username = 'taoting'

    accept_problems = {}
    res = VjudgeSpider.get_user_info(oj_username, accept_problems)
    f = 0
    for i in res['data']:
        if i['oj'] == 'jisuanke' and i['problem_pid'] == 'T1001' and i['accept_time'] == '2019-11-11 11:54:57':
            f = 1
            break
    assert f

    accept_problems = {'jisuanke-T1001': '2019-11-11 11:54:57'}
    res = VjudgeSpider.get_user_info(oj_username, accept_problems)
    f = 0
    for i in res['data']:
        if i['oj'] == 'jisuanke' and i['problem_pid'] == 'T1001' and i['accept_time'] == '2019-11-11 11:54:57':
            f = 1
            break
    assert not f
