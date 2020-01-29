from app.spiders.hdu_spider import HduSpider
from app.test_base import client


def test_hdu_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = 'taoting1234'

    accept_problems = {}
    res = HduSpider.get_user_info(oj_username, accept_problems)
    f = 0
    for i in res:
        if i['oj'] == 'hdu' and i['problem_pid'] == '6703' and i['accept_time'] == '2019-08-24 10:39:31':
            f = 1
            break
    assert f

    accept_problems = {'hdu-6703': '2019-08-24 10:39:31'}
    res = HduSpider.get_user_info(oj_username, accept_problems)
    f = 0
    for i in res:
        if i['oj'] == 'hdu' and i['problem_pid'] == '6703' and i['accept_time'] == '2019-08-24 10:39:31':
            f = 1
            break
    assert not f


def test_hdu_problem_info(client):
    assert HduSpider.get_problem_info('1000')['rating'] == 1500
