from app.spiders.nowcoder_spider import NowcoderSpider
from app.test_base import client


def test_nowcoder_user_info(client):
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = 'Kwords'

    test_data = {
        'oj': 'nowcoder',
        'problem_pid': '201841',
        'accept_time': '2020-01-20 17:40:13'
    }
    accept_problems = {}
    res = NowcoderSpider().get_user_info(oj_username, accept_problems)
    assert test_data in res['data']

    oj_username.oj_username = '3538959'
    accept_problems = {'nowcoder-201841': '2020-01-20 17:40:13'}
    res = NowcoderSpider().get_user_info(oj_username, accept_problems)
    assert test_data not in res['data']
