from app.spiders.loj_spider import LojSpider
from app.test_base import client


def test_zucc_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = 'Hile_M'

    test_data = {
        'oj': 'loj',
        'problem_pid': '133',
        'accept_time': '2020-01-29 04:38:58'
    }
    accept_problems = {}
    res = LojSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    accept_problems = {'loj-133': '2020-01-29 04:38:58'}
    res = LojSpider().get_user_info(oj_username, accept_problems)
    assert test_data not in res['data']
