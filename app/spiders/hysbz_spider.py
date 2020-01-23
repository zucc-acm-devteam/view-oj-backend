import json
import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class HysbzHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'host': 'www.lydsy.com'
        }
        self.headers.update(headers)


class HysbzSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'http://www.lydsy.com/JudgeOnline/userinfo.php?user={}'.format(username)
        res = HysbzHttp().get(url=url)
        accept_problem_list = re.findall(r'p\((\d+)\)', res.text)
        return accept_problem_list

    def get_problem_info(self, problem_id):
        url = 'https://www.lydsy.com/JudgeOnline/problem.php?id={}'.format(problem_id)
        headers = {
            'host': 'www.lydsy.com',
            'referer': 'https://www.lydsy.com/JudgeOnline/problemset.php'
        }
        res = HysbzHttp().get(url=url, headers=headers)

        try:
            total = int(re.search(r'<span class=green>Submit: </span>(\d+)&nbsp;&nbsp;', res.text).group(1))
            accept = int(re.search(r'<span class=green>Solved: </span>(\d+)<br>', res.text).group(1))
            rating = calculate_problem_rating(total, accept)
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'Hile_M'
    print(HysbzSpider().get_user_info(oj_username))
