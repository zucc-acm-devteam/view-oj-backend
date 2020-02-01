from app.spiders.codeforces_spider import CodeforcesSpider
from app.test_base import client


def test_codeforces_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = 'taoting'

    test_data = {
        'oj': 'codeforces',
        'problem_pid': '102397F',
        'accept_time': '2019-12-06 14:15:37'
    }
    accept_problems = {}
    res = CodeforcesSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    accept_problems = {'codeforces-102397F': '2019-12-06 14:15:37'}
    res = CodeforcesSpider().get_user_info(oj_username, accept_problems)

    assert test_data not in res['data']


def test_codeforces_problem_info(client):
    from app import create_app
    create_app().app_context().push()
    # 题目
    assert CodeforcesSpider().get_problem_info('1272F')['rating'] == 2400
    # gym
    assert CodeforcesSpider().get_problem_info('102397D')['rating'] == 1200
