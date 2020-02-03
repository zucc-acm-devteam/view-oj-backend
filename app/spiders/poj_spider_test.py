from app.spiders.poj_spider import PojSpider
from app.test_base import client


def test_poj_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = 'Hile_M'

    test_data = {
        'oj': 'poj',
        'problem_pid': '1064',
        'accept_time': '2019-12-07 00:30:03'
    }
    accept_problems = {}
    res = PojSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    accept_problems = {'poj-1064': '2019-12-07 00:30:03'}
    res = PojSpider().get_user_info(oj_username, accept_problems)
    assert test_data not in res['data']
