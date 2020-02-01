from app.spiders.luogu_spider import LuoguSpider
from app.test_base import client


def test_luogu_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()

    test_data = {
        'oj': 'luogu',
        'problem_pid': '1001',
        'accept_time': '2017-10-19 10:45:47'
    }
    # uid
    oj_username.oj_username = '62916'
    accept_problems = {}
    res = LuoguSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    # 用户名
    oj_username.oj_username = 'taoting'
    accept_problems = {}
    res = LuoguSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']


def test_luogu_problem_info(client):
    assert LuoguSpider().get_problem_info('1001')['rating'] == 1500
