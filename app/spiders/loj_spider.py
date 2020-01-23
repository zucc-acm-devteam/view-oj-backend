import json
import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class LojSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        uid = LojSpider._get_user_id(username)
        url = 'https://loj.ac/user/{}'.format(uid)
        res = SpiderHttp().get(url=url)
        accept_problem_list = re.findall(r'<a href="/problem/(\d+)">', res.text)
        return accept_problem_list

    def get_problem_info(self, problem_id):
        try:
            url = 'http://loj.ac/problems/search?keyword={}'.format(problem_id)
            res = SpiderHttp().get(url=url)
            data = re.findall(r'<td>(\d+)</td>\n.*<td>(\d+)</td>', res.text)[0]
            accept = int(data[0])
            total = int(data[1])
            rating = int(calculate_problem_rating(total, accept))
        except:
            rating = DEFAULT_PROBLEM_RATING
        return {'rating': rating}

    @staticmethod
    def _get_user_id(username):
        url = 'http://loj.ac/find_user?nickname={}'.format(username)
        res = SpiderHttp().get(url=url)
        uid = re.findall(r'user/(\d+)', res.url)[0]
        return uid


if __name__ == '__main__':
    print(LojSpider().get_problem_info('1'))
