from app.spiders.vjudge_spider import VjudgeSpider
from app.test_base import client


def test_vjudge_user_info(client):
    from app import create_app
    from app.models.oj_username import OJUsername
    create_app().app_context().push()
    oj_username = OJUsername()
    oj_username.oj_username = 'taoting'

    test_data = {
        'oj': 'jisuanke',
        'problem_pid': 'T1001',
        'accept_time': '2019-11-11 11:54:57'
    }

    accept_problems = {}
    res = VjudgeSpider.get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    accept_problems = {'jisuanke-T1001': '2019-11-11 11:54:57'}
    res = VjudgeSpider.get_user_info(oj_username, accept_problems)
    assert test_data not in res['data']
