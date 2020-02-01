from app.spiders.hdu_spider import HduSpider
from app.test_base import client


def test_hdu_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = 'taoting1234'

    test_data = {
        'oj': 'hdu',
        'problem_pid': '6703',
        'accept_time': '2019-08-24 10:39:31'
    }

    accept_problems = {}
    res = HduSpider.get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    accept_problems = {'hdu-6703': '2019-08-24 10:39:31'}
    res = HduSpider.get_user_info(oj_username, accept_problems)
    assert test_data not in res['data']


def test_hdu_problem_info(client):
    assert HduSpider.get_problem_info('1000')['rating'] == 1500
