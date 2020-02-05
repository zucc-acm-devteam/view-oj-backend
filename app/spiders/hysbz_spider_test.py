from app.spiders.hysbz_spider import HysbzSpider
from app.test_base import client


def test_hysbz_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = 'Hile_M'

    test_data = {
        'oj': 'hysbz',
        'problem_pid': '1101',
        'accept_time': '2019-12-09 20:29:09'
    }
    accept_problems = {}
    res = HysbzSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    accept_problems = {'hysbz-1101': '2019-12-09 20:29:09'}
    res = HysbzSpider().get_user_info(oj_username, accept_problems)
    assert test_data not in res['data']
