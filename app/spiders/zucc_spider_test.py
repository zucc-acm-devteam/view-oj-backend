from app.spiders.zucc_spider import ZuccSpider
from app.test_base import client


def test_zucc_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = '31801054'

    test_data = {
        'oj': 'zucc',
        'problem_pid': '2112',
        'accept_time': '2019-09-19 20:45:56'
    }
    accept_problems = {}
    res = ZuccSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    accept_problems = {'zucc-2112': '2019-09-19 20:45:56'}
    res = ZuccSpider().get_user_info(oj_username, accept_problems)
    assert test_data not in res['data']
