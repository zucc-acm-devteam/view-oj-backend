from app.spiders.pintia_spider import PintiaSpider
from app.test_base import client


def test_pintia_user_info(client):
    from app import create_app
    from app.models.oj_username import OJUsername
    create_app().app_context().push()
    oj_username = OJUsername()
    oj_username.oj_username = '757795210@qq.com'
    oj_username.oj_password = '7110100408DL'

    test_data = {
        'oj': 'pintia',
        'problem_pid': 'L-L1-001',
        'accept_time': '2018-12-07 13:45:37'
    }

    accept_problems = {}
    res = PintiaSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    accept_problems = {'pintia-L-L1-001': '2018-12-07 13:45:37'}
    res = PintiaSpider().get_user_info(oj_username, accept_problems)
    assert test_data not in res['data']
